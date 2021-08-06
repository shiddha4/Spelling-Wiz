# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
words = open('words/words.txt', 'r')
word_list = []
con_grade_level = str(grade)
for word in words:
    for letter in word:
        if con_grade_level in letter:
            word_list.append(word.replace(f',{con_grade_level}', ''))
print(con_grade_level)
print(word_list)

word = random.choice(word_list).strip()
return word


