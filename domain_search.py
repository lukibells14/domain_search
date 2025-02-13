# import streamlit as st
# import pandas as pd
# from duckduckgo_search import DDGS

# def extract_domain(url):
#     """Extract the domain from a URL (text between // and the next /)."""
#     start = url.find("//") + 2  
#     end = url.find("/", start)  
#     return url[start:end] if end != -1 else url[start:]

# def find_company_domains(company_name):
#     """Search DuckDuckGo using the DDGS library and extract domains."""
#     with DDGS() as ddgs:
#         results = [r for r in ddgs.text(company_name, max_results=5)]
#         domains = [extract_domain(result['href']) for result in results if result.get('href')]
#         return domains[:5] if domains else ["No results found"]

# # Streamlit UI
# st.title("Company Domain Finder")

# # Tabs for Single & Bulk Search
# tab1, tab2 = st.tabs(["🔍 Single Search", "📂 Bulk Search"])

# # SINGLE SEARCH
# with tab1:
#     st.subheader("Search a Single Company")
#     single_company = st.text_input("Enter Company Name")

#     if st.button("Search"):
#         if single_company:
#             with st.spinner("Searching..."):
#                 domains = find_company_domains(single_company)

#             # Display domains in a table
#             df_display = pd.DataFrame({"Index": range(len(domains)), "Domain": domains})
#             st.table(df_display)

#             # Dropdown for selecting index
#             selected_index = st.selectbox("Select the correct domain (by index):", range(len(domains)))

#             # Store selected domain
#             selected_domain = domains[selected_index]

#             st.success(f"Selected Domain: {selected_domain}")

#             # Create dataframe for download
#             result_df = pd.DataFrame([{"Company Name": single_company, "Selected Domain": selected_domain}])

#             st.download_button("Download Result", 
#                                result_df.to_csv(index=False).encode("utf-8"),
#                                file_name="single_company_domain.csv",
#                                mime="text/csv")

# # BULK SEARCH
# with tab2:
#     st.subheader("Upload an Excel file for Bulk Search")
#     uploaded_file = st.file_uploader("Upload an Excel file (Must contain a 'Company Name' column)", type=["xlsx"])

#     if uploaded_file:
#         df = pd.read_excel(uploaded_file)

#         if "Company Name" not in df.columns:
#             st.error("Excel file must contain a column named 'Company Name'.")
#         else:
#             # Session state for tracking progress
#             if "current_index" not in st.session_state:
#                 st.session_state.current_index = 0
#             if "selected_domains" not in st.session_state:
#                 st.session_state.selected_domains = []

#             current_index = st.session_state.current_index

#             # Stop if all companies are processed
#             if current_index >= len(df):
#                 st.success("All companies processed!")
#                 result_df = pd.DataFrame(st.session_state.selected_domains)
#                 st.dataframe(result_df)

#                 st.download_button("Download Excel",
#                                    result_df.to_csv(index=False).encode("utf-8"),
#                                    file_name="selected_domains.csv",
#                                    mime="text/csv")
#             else:
#                 company_name = df.loc[current_index, "Company Name"]

#                 st.subheader(f"Searching: {company_name}")
#                 with st.spinner("Searching..."):
#                     domains = find_company_domains(company_name)

#                 # Display domains in a table
#                 df_display = pd.DataFrame({"Index": range(len(domains)), "Domain": domains})
#                 st.table(df_display)

#                 # Dropdown for selecting index
#                 selected_index = st.selectbox("Select the correct domain (by index):", 
#                                               range(len(domains)), key=current_index)

#                 selected_domain = domains[selected_index]

#                 # Next button
#                 if st.button("Next"):
#                     st.session_state.selected_domains.append({"Company Name": company_name, "Selected Domain": selected_domain})
#                     st.session_state.current_index += 1
#                     st.experimental_rerun()


import streamlit as st
import pandas as pd
from duckduckgo_search import DDGS

def extract_domain(url):
    """Extract the domain from a URL (text between // and the next /)."""
    start = url.find("//") + 2  
    end = url.find("/", start)  
    return url[start:end] if end != -1 else url[start:]

def find_company_domains(company_name):
    """Search DuckDuckGo using the DDGS library and extract domains."""
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(company_name, max_results=5)]
        domains = [extract_domain(result['href']) for result in results if result.get('href')]
        return domains[:5] if domains else ["No results found"]

# Streamlit UI
st.title("Company Domain Finder")

# Tabs for Single & Bulk Search
tab1, tab2 = st.tabs(["🔍 Single Search", "📂 Bulk Search"])

# SINGLE SEARCH
with tab1:
    st.subheader("Search a Single Company")
    single_company = st.text_input("Enter Company Name")

    if st.button("Search"):
        if single_company:
            with st.spinner("Searching..."):
                st.session_state.single_domains = find_company_domains(single_company)
                st.session_state.single_search_done = True

    # Prevent searching again if already done
    if st.session_state.get("single_search_done", False):
        domains = st.session_state.get("single_domains", [])
        
        # Display domains in a table
        df_display = pd.DataFrame({"Domain": domains})
        st.table(df_display)

        # Dropdown for selecting domain
        selected_domain = st.selectbox("Select the correct domain:", domains)

        if selected_domain:
            st.success(f"Selected Domain: {selected_domain}")

            # Create dataframe for download
            result_df = pd.DataFrame([{"Company Name": single_company, "Selected Domain": selected_domain}])

            st.download_button("Download Result", 
                               result_df.to_csv(index=False).encode("utf-8"),
                               file_name="single_company_domain.csv",
                               mime="text/csv")

# BULK SEARCH
with tab2:
    st.subheader("Upload an Excel file for Bulk Search")
    uploaded_file = st.file_uploader("Upload an Excel file (Must contain a 'Company Name' column)", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        if "Company Name" not in df.columns:
            st.error("Excel file must contain a column named 'Company Name'.")
        else:
            # Initialize session state variables
            if "current_index" not in st.session_state:
                st.session_state.current_index = 0
            if "selected_domains" not in st.session_state:
                st.session_state.selected_domains = []
            if "bulk_search_done" not in st.session_state:
                st.session_state.bulk_search_done = False
            if "bulk_domains" not in st.session_state:
                st.session_state.bulk_domains = {}

            current_index = st.session_state.current_index

            # Stop if all companies are processed
            if current_index >= len(df):
                st.success("All companies processed!")
                result_df = pd.DataFrame(st.session_state.selected_domains)
                # st.dataframe(result_df)
                st.dataframe(result_df, width=800)

                st.download_button("Download Excel",
                                   result_df.to_csv(index=False).encode("utf-8"),
                                   file_name="selected_domains.csv",
                                   mime="text/csv")
            else:
                company_name = df.loc[current_index, "Company Name"]

                st.subheader(f"Searching: {company_name}")

                # Only search if not already searched
                if not st.session_state.bulk_search_done or company_name not in st.session_state.bulk_domains:
                    with st.spinner("Searching..."):
                        st.session_state.bulk_domains[company_name] = find_company_domains(company_name)
                    st.session_state.bulk_search_done = True

                # Retrieve stored domains
                domains = st.session_state.bulk_domains.get(company_name, ["No results found"])

                # Display domains in a table
                # df_display = pd.DataFrame({"Domain": domains})
                # st.table(df_display)
                # Display domains in a resizable table
                st.dataframe(pd.DataFrame({"Domain": domains}), use_container_width=True, height=200)


                # Dropdown for selecting domain
                selected_domain = st.selectbox(f"Select the correct domain for {company_name}:", domains, key=current_index)

                # Next button
                if st.button("Next"):
                    st.session_state.selected_domains.append({"Company Name": company_name, "Selected Domain": selected_domain})
                    st.session_state.current_index += 1
                    st.session_state.bulk_search_done = False  # Reset flag for next search
                    st.experimental_rerun()

