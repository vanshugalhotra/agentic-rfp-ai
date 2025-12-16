import streamlit as st

st.title("RFP URL Submission")

st.markdown("Enter or upload a list of RFP URLs to queue them for processing. One URL per line.")

# Text area for manual entry
urls_text = st.text_area(
    label="Manual URL entry (collapsed)",  # Label only for accessibility
    label_visibility="collapsed",
    placeholder="Paste RFP URLs here, one per line...\ne.g., https://example.com/rfp/123\nhttps://example.com/rfp/456",
    height=200,
    help="Enter multiple URLs manually. Empty lines will be ignored."
)

# File uploader for .txt list
uploaded_file = st.file_uploader(
    label="Upload URL list (collapsed)",
    label_visibility="collapsed",
    type=["txt"],
    accept_multiple_files=False,
    help="Upload a plain text file (.txt) containing URLs, one per line."
)

# Submit button in a right-aligned column
col1, col2 = st.columns([3, 1])
with col2:
    submit = st.button("Submit", type="primary", use_container_width=True)

if submit:
    urls = []

    if urls_text:
        urls.extend([u.strip() for u in urls_text.splitlines() if u.strip()])

    if uploaded_file is not None:
        try:
            file_urls = uploaded_file.read().decode("utf-8").splitlines()
            urls.extend([u.strip() for u in file_urls if u.strip()])
        except Exception:
            st.error("Failed to read the uploaded file. Ensure it's a valid .txt file with UTF-8 encoding.")
            st.stop()

    if not urls:
        st.warning("No valid URLs were provided. Please enter or upload at least one URL.")
    else:
        # Remove duplicates while preserving order
        unique_urls = []
        seen = set()
        for url in urls:
            if url not in seen:
                unique_urls.append(url)
                seen.add(url)

        st.session_state.urls = unique_urls

        st.success(f"**{len(unique_urls)} URL(s)** queued successfully.")
        if len(urls) > len(unique_urls):
            st.info(f"{len(urls) - len(unique_urls)} duplicate(s) were removed.")