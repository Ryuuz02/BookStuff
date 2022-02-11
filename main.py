# Import Statements
import urllib.request


# Gets the url for the stopwords, then puts those words into a list
sw_url = 'https://moss.cs.iit.edu/stopwords.txt'
sw_text = urllib.request.urlopen(sw_url).read().decode()
stopwords = sw_text.split()

# Finds the book we are working with, then gets its text
url = "https://www.gutenberg.org/files/164/164.txt"
book_text = urllib.request.urlopen(url).read().decode()

# Finds the beginning and the end of the book
begin_index = book_text.index("Chapter I".upper())
end_index = book_text.index("End of the Project Gutenberg EBook")
# Then takes the slice in between
parsed_text = book_text[begin_index:end_index]

# Splits the text into a list of its words
split_text = parsed_text.split()

# Finds where all the chapter markers are, so we can later take them out
chapter_indexes = []
for word in range(0, len(split_text)):
    if split_text[word] == "CHAPTER":
        chapter_indexes.append(word)

# For each Chapter in the book, will take out that chapter and any extra words after (i.e. the chapter # and the title
# of the chapter)
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

# String containing all the "filler" characters that could be used that we want to get rid of
extra_chars = "\"'?!.-()_[]`;,:|\\/"

# For each word in the book
for word in range(0, len(split_text)):
    # Strips the ends of it of extra characters
    iterated_word = split_text[word].lower().strip(extra_chars)
    # While there are extra characters still in the word
    for char in extra_chars:
        while char in iterated_word:
            # Takes them out
            iterated_word = iterated_word.replace(char, "")
    # Then replaces its value
    split_text[word] = iterated_word

# Set of unique words
unique_words = set(split_text)

# Word count dict
word_count = {}
# For each word in the book, adds 1 to the value of its associated key in the word_count
for word in split_text:
    try:
        word_count[word] += 1
    except KeyError:
        word_count[word] = 1

# Removes the stopwords in the word_count
sw_removed_word_count = {}
for key in word_count.keys():
    if key not in stopwords:
        sw_removed_word_count[key] = word_count[key]

# Turns that into a set for stopword removed unique words
sw_removed_unique_words = set(sw_removed_word_count)

# Sorts the word count alphabetically
sorted_word_count = sorted(sw_removed_word_count)

