from pyresparser import ResumeParser

data = ResumeParser('sachin_resume.pdf',
                    custom_regex=r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]').get_extracted_data()
print(data)
