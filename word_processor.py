import re
import logging


def word_to_sub(text, logger: logging.Logger):
    is_chinese = False
    if re.search(u'[\u4e00-\u9fff]', text):
        is_chinese = True
    sub_text = text
    #Process phone num
    phone_number_str_list : list[str] = re.findall(r"\d{4}\s\d{4}|\d{8}", sub_text)
    for phone_num in phone_number_str_list:
        _phone_num = " ".join(list(filter(type(int),  re.split(r"(.*?\d)", phone_num))))
        sub_text = re.sub(phone_num, _phone_num, sub_text)
        
    #Process email
    email_str_list: list[str] = re.findall(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6}", sub_text)
    for email in email_str_list:
        email_list = email.split("@", 1)
        email_list[1] = email_list[1].upper()
        _email = " at ".join(email_list)
        _email = re.sub(r"\.", " dot ", _email)
        sub_text = re.sub(email, _email, sub_text)
    
    #Process link tag
    link_tag_str_list: list[str] = re.findall(r"(\[LINK\].*?\[LINK\])", sub_text)
    for link_tag in link_tag_str_list:
        try:
            link_name_tag : str = re.findall(r"(\[NAME=.*?\])", link_tag)[0] # expect only one name
            link_name = link_name_tag.split("=", 1)[1] #Get the name
            link_name = re.sub(r"\]", "", link_name) #Remove a remaining close tag
            sub_text = re.sub(link_tag, link_name, sub_text)
        except Exception as e:
            # Failed parse handle
            sub_text = re.sub(link_tag, " ", sub_text)
            logger.error(f"Failed to process link tag {e}")
            
    #Process url link
    url_link_str_list: list[str] = re.findall(r"(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?", sub_text)
    for url in url_link_str_list:
        url = re.sub(":", " colon ", url)
        url = re.sub("/", " slash ", url)
        url = re.sub(r"\.", " dot ", url)
        url = re.sub("_", " underscore ", url)
        url = re.sub("-", " hyphen ", url)
    #Process Tag Content
    sub_text = re.sub(r"(\[PDF\].*?\[PDF\])", " this file " if is_chinese is False else " 這個檔案 ", sub_text)
    sub_text = re.sub(r"(\[IMG\].*?\[IMG\])", " this photo " if is_chinese is False else " 這幅圖片 ", sub_text)
    sub_text = re.sub(r"\[TABLE\]|\[SPLIT\]", " ", sub_text)
    sub_text = re.sub(r"\[ITALIC\]|\[UNDERLINE\]|.*?AUTOOPEN|\[NEWPAGE\]", "", sub_text)
    
    #Filter all markdown symbol
    sub_text = re.sub(r"(?:__|[*#])|\[(.*?)\]\(.*?\)", "", sub_text)
    logger.info(f"Process text success: {sub_text}")
    return sub_text
