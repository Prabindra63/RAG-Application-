import os

import streamlit as st

from dotenv import (
    load_dotenv,
)

from backend.service import (
    ask_question,
    document_status,
    index_pdf,
    reset_document,
    save_uploaded_pdf,
)

load_dotenv()

st.set_page_config(
    page_title="FinReport AI",
    page_icon="📊",
    layout="wide",
)

api_key = os.getenv(
    "GOOGLE_API_KEY"
)

if not api_key:

    st.error(
        "GOOGLE_API_KEY missing in .env"
    )

    st.stop()

if (
    "messages"
    not in st.session_state
):
    st.session_state.messages = []

status = document_status()

with st.sidebar:

    st.title(
        "📊 FinReport AI"
    )

    uploaded = st.file_uploader(
        "Upload Financial Report",
        type=["pdf"],
    )

    if uploaded:

        if st.button(
            "Process PDF"
        ):

            try:

                with st.spinner(
                    "Indexing..."
                ):

                    path = (
                        save_uploaded_pdf(
                            uploaded.read(),
                            uploaded.name,
                        )
                    )

                    result = index_pdf(
                        path,
                        uploaded.name,
                    )

                st.success(
                    f"Indexed {result['num_pages']} pages"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    str(e)
                )

    st.divider()

    if status:

        st.write(
            f"📄 {status['filename']}"
        )

        st.write(
            f"Pages: {status['num_pages']}"
        )

        st.write(
            f"Chunks: {status['num_chunks']}"
        )

        if st.button(
            "Reset Document"
        ):
            reset_document()
            st.session_state.messages = []
            st.rerun()

st.title(
    "📊 FinReport AI"
)

st.caption(
    "Ask questions about annual and quarterly reports."
)

if not status:

    st.info(
        "Upload a PDF first."
    )

else:

    for msg in st.session_state.messages:

        with st.chat_message(
            msg["role"]
        ):

            st.markdown(
                msg["content"]
            )

            if (
                msg["role"]
                == "assistant"
                and msg.get(
                    "sources"
                )
            ):

                with st.expander(
                    "Sources"
                ):

                    for src in msg[
                        "sources"
                    ]:

                        st.write(
                            f"Page {src['page']} "
                            f"(score={src['score']:.3f})"
                        )

                        st.code(
                            src[
                                "content"
                            ][
                                :400
                            ]
                        )

    question = st.chat_input(
        "Ask a question..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message(
            "user"
        ):
            st.markdown(
                question
            )

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Thinking..."
            ):

                result = (
                    ask_question(
                        question,
                        api_key,
                    )
                )

                answer = result[
                    "answer"
                ]

                sources = result[
                    "sources"
                ]

                st.markdown(
                    answer
                )

                if sources:

                    with st.expander(
                        "Sources"
                    ):

                        for src in (
                            sources
                        ):

                            st.write(
                                f"Page {src['page']} "
                                f"(score={src['score']:.3f})"
                            )

                            st.code(
                                src[
                                    "content"
                                ][
                                    :400
                                ]
                            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources,
            }
        )