def getGender(sex="Unknown"):
    if sex is 'm':
        sex = 'male'
    elif sex is 'f':
        sex = 'female'
    print(sex)

getGender('m')
getGender('f')
getGender()
