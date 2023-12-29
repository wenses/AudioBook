import PyPDF2 as pdf2

class ReadBook:

    def single_page(book,page_number):
        pdfreader=pdf2.PdfReader(open(book,'rb'))

        return pdfreader.pages[page_number-1].extract_text()

    def section_pages(book,starting_page,ending_page):

        txt_list=[]

        for page in range(starting_page,ending_page+1):
            pdfreader=pdf2.PdfReader(open(book,'rb'))

            ptxt=pdfreader.pages[page-1].extract_text()

            txt_list.append(ptxt)

        return txt_list

    def all_pages(book):

        txt_list=[]

        pdfreader=pdf2.PdfReader(open(book,'rb'))

        last_page = len(pdfreader.pages) 


        for page in range(1,last_page+1):
            ptxt=pdfreader.pages[page-1].extract_text()

            txt_list.append(ptxt)


        return txt_list

    def get_pages(book):
        pdfreader=pdf2.PdfReader(open(book,'rb'))

        return len(pdfreader.pages)


