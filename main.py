import urllib.request

sw_url = 'https://moss.cs.iit.edu/stopwords.txt'
sw_text = urllib.request.urlopen(sw_url).read().decode()
stopwords = sw_text.split()

url = "https://www.gutenberg.org/files/164/164.txt"
book_text = urllib.request.urlopen(url).read().decode()
begin_index = book_text.index("Chapter I".upper())
end_index = book_text.index("End of the Project Gutenberg EBook")
parsed_text = book_text[begin_index:end_index]

split_text = parsed_text.split()
chapter_indexes = []
for word in range(0, len(split_text)):
    if split_text[word] == "CHAPTER":
        chapter_indexes.append(word)

extras = 0
for word in range(0, len(chapter_indexes)):
    running = True
    extra_words = -1
    while running:
        next_word = split_text[chapter_indexes[word] - word - extras]
        if next_word == next_word.upper() and len(next_word) == 1:
            next_next_word = split_text[chapter_indexes[word] + 1 - word - extras]
            if next_next_word == next_next_word.upper():
                extra_words += 2
                split_text.pop(chapter_indexes[word] - word - extras)
                split_text.pop(chapter_indexes[word] - word - extras)
            else:
                running = False
        elif next_word == next_word.upper():
            extra_words += 1
            split_text.pop(chapter_indexes[word] - word - extras)
        else:
            running = False
    extras += extra_words
extra_chars = "\"'?!.-"
for word in range(0, len(split_text)):
    iterated_word = split_text[word].lower().strip('\'"?!.-')
    for char in extra_chars:
        while char in iterated_word:
            iterated_word = iterated_word.replace(char, "")
    split_text[word] = iterated_word
unique_words = set(split_text)
word_count = {}
for word in split_text:
    try:
        word_count[word] += 1
    except KeyError:
        word_count[word] = 1
print(word_count)
