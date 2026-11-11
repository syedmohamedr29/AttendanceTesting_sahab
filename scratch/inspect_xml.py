import zipfile

with zipfile.ZipFile('CompanyDefault_DTO_Validation_TestCases.xlsx', 'r') as z:
    for name in z.namelist():
        if 'sheet1' in name:
            content = z.read(name).decode('utf-8')
            # find dataValidation and autoFilter tags
            idx_dv = content.find('dataValidation')
            if idx_dv != -1:
                print('--- dataValidation XML ---')
                print(content[idx_dv-20:idx_dv+400])
            idx_af = content.find('autoFilter')
            if idx_af != -1:
                print('--- autoFilter XML ---')
                print(content[idx_af-20:idx_af+100])

