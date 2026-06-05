import os

import streamlit as st
from dotenv import load_dotenv

from backend.service import (
    ask_question,
    document_status,
    index_pdf,
    reset_document,
    save_uploaded_pdf,
)

load_dotenv()


def render_citations(sources):
    with st.expander("📖 Sources"):
        for i, src in enumerate(sources, start=1):
            st.markdown(
                f"**Source {i} | Page {src['page']} | Score {src['score']:.3f}**"
            )
            st.code(src["content"])


def process_question(question, api_key):
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = ask_question(
                question=question,
                api_key=api_key,
            )

            st.markdown(result["answer"])

            if result.get("sources"):
                render_citations(result["sources"])

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": result["answer"],
                    "citations": result.get("sources", []),
                }
            )


def main():
    st.set_page_config(
        page_title="FinReport AI",
        page_icon="📊",
        layout="wide",
    )

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        st.error(
            "GOOGLE_API_KEY not found. Add it to your .env file."
        )
        st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    status = document_status()
    metadata = status if status.get("ready") else None

    # =========================
    # Sidebar
    # =========================

    with st.sidebar:
        st.title("📊 FinReport AI")

        uploaded_file = st.file_uploader(
            "Upload Financial Report",
            type=["pdf"],
        )

        if uploaded_file:
            if st.button(
                "Process PDF",
                use_container_width=True,
            ):
                with st.spinner("Processing PDF..."):
                    path = save_uploaded_pdf(
                        uploaded_file.read(),
                        uploaded_file.name,
                    )

                    result = index_pdf(
                        path,
                        filename=uploaded_file.name,
                    )

                st.success(
                    f"Indexed {result['num_pages']} pages "
                    f"and {result['num_chunks']} chunks."
                )

                st.rerun()

        st.divider()

        if metadata:
            st.subheader("Current Document")

            st.write(f"📄 {metadata['filename']}")
            st.write(f"Pages: {metadata['num_pages']}")
            st.write(f"Chunks: {metadata['num_chunks']}")

            if st.button(
                "🗑 Reset Document",
                use_container_width=True,
            ):
                reset_document()
                st.session_state.messages = []
                st.rerun()

        st.divider()

        if st.button(
            "🧹 Clear Chat",
            use_container_width=True,
        ):
            st.session_state.messages = []
            st.rerun()

    # =========================
    # Main Area
    # =========================

    st.title("📊 FinReport AI")

    st.caption(
        "Upload a financial report and ask questions about it."
    )

    if not metadata:
        st.info(
            "Upload and process a PDF from the sidebar to begin."
        )
        return

    # Chat History

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            if (
                msg["role"] == "assistant"
                and msg.get("citations")
            ):
                render_citations(
                    msg["citations"]
                )

    # Chat Input

    if question := st.chat_input(
        "Ask about the report..."
    ):
        process_question(
            question,
            api_key,
        )


if __name__ == "__main__":
    main()