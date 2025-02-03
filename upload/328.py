import streamlit as st
import openai
import os
import textwrap
from PyPDF2 import PdfReader
import deepl
import tiktoken


def summarize_PDF_file(pdf_file, lang, trans_checked):
    if (pdf_file is not None):
        st.write("PDF 문서를 요약 중입니다. 잠시만 기다려 주세요.")
        reader = PdfReader(pdf_file)

        text_summarizes = []

        for page in reader.pages:
            page_text = page.extract_text()
            summary = summarize_text(page_text, lang)
            text_summarizes.append(summary)

        token_num, final_summary = summarize_text_final(text_summarizes, lang)

        if final_summary != "":
            shorten_final_summary = textwrap.shorten(final_summary, 250, placeholder=' [..이하생략 ..]')

            st.write('-최종 요약(측약);', shorten_final_summary)

            if trans_checked:
                trans_result = translate_e_to_k(final_summary)
                shorten_trans_result = textwrap.shorten(trans_result, 200, placeholder=' [..이하생략 ..]')
                st.write('한국어 요약(축약):', shorten_trans_result)
        else:
            st.write("-통합한 용약문의 토큰 수가 커서 요약할 수 없습니다.")

def summarize_text(user_text, lang="en"):
    api_key = os.environ["OPENAI_API_KEY"]
    openai.api_key = api_key

    if lang == "en":
        messages = [
            {"role" : "system", "content" : "You are a helpful assistant in the summary."},
            {"role" : "user", "content" : f"Summarize the following. \n {user_text}"}
        ]
    elif lang == "ko":
        messages = [
            {"role" : "system", "content" : "You are a helpful assistant in the summary."},
            {"role" : "user", "content" : f"Summarize the following in korea. \n {user_text}"}
        ]
    response = openai.chat.completions.create(
        model = "gpt-3.5-turbo", # GPT 모델 선택
        messages = messages, # 전달할 메시지 지정
        temperature = 0.8, # 완성의 다양성을 조절하는 온도 설정
        max_tokens = 2000, # 응답 최대 토큰 수 지정
        n=1 # 응답 개수 지정
    )
# assistant_reply = response.choices[0].message.content
# print(assistant_reply)
    summary = response.choices[0].message.content
    return summary

def summarize_text_final(text_list, lnag = "en"):
    joined_summary = " ".join(text_list)

    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    token_num = len(enc.encode(joined_summary))

    req_max_token = 2000
    final_summary = ""
    if token_num < req_max_token:
        final_summary = summarize_text(joined_summary, lnag)

    kjreturn token_num, final_summary\

# def translate_deepl_e_to_k(text):
#     auth_key = os.environ["DEEPL_AUTH_KEY"]
#     translate = deepl.Translator(auth_key)
#
#     result = translate.translate_text(text, target_lang="KO")
#
#     return result.text
def translate_e_to_k(text):
    openai.api_key = os.environ["OPENAI_API_KEY"]

    user_content = f"Translate th following English sentences into korean.\n {text}"
    messages = [{"role":"user", "content":user_content}]

    response =  openai.chat.completions.create(
        model = "gpt-3.5-turbo", # GPT 모델 선택
        messages = messages, # 전달할 메시지 지정
        temperature = 0.3, # 완성의 다양성을 조절하는 온도 설정
        max_tokens = 2000, # 응답 최대 토큰 수 지정
        n=1 # 응답 개수 지정
    )
    assistant_reply = response.choices[0].message.content
    return assistant_reply


st.title("PDF 문서를 요약하는 웹 앱")
uploaded_file = st.file_uploader("PDF 파일을 업로드 하세요.", type = 'pdf')
radio_selected_lang = st.radio('PDF 문서 언어', ['한국어', '영어'], index = 1, horizontal =True)

if radio_selected_lang =='영어':
    lang_code = 'en'
    checked =st.checkbox('한국어 번역 추가')
else:
    lang_code = 'ko'
    checked = False

clicked = st.button('PDF 문서 요약')

if clicked:
    summarize_PDF_file(uploaded_file, lang_code, checked)

