# These are the emails you will be censoring. The open() function is opening the text file that the emails are contained in and the .read() method is allowing us to save their contexts to the following variables:
email_one = open("email_one.txt", "r").read()
email_two = open("email_two.txt", "r").read()
email_three = open("email_three.txt", "r").read()
email_four = open("email_four.txt", "r").read()

proprietary_terms = ["she", "personality matrix", "sense of self", "self-preservation", "learning algorithm", "her", "herself"]
negative_words = ["concerned", "behind", "danger", "dangerous", "alarming", "alarmed", "out of control", "help", "unhappy", "bad", "upset", "awful", "broken", "damage", "damaging", "dismal", "distressing", "distressed", "concerning", "horrible", "horribly", "questionable"]

#test_text = """last month improving the 
#learning algorithms."""

def censor_text(text, word):
  censored = ""
  censored_text = ""
  censored_text_lines = []
  punctuation_marks = ['.', ',', '(', ')', '!', '?', '\'', '\"', ':', ';', '/']

  for letter in word:
    censored += "*"

  text_lines = text.split('\n')
  #print(text_lines)
  for line in text_lines:
    censored_line = line
    if (censored_line == ''):
      censored_text_lines.append(censored_line)
    else:      
      for i in range(3):
        word_to_find = word      
        if (i == 1):
          word_to_find = word[0].upper() + word[1:]
        elif (i == 2):
          word_to_find = word.upper()

        while_counter = 0
        while (censored_line.find(word_to_find) > -1):
          while_counter += 1
          word_index = censored_line.find(word_to_find)
          char_before_word = censored_line[word_index - 1]
          char_after_word = censored_line[word_index + len(word_to_find)]
          
          word_found = False
          if (word_index == 0):
            if (char_after_word == ' ' or punctuation_marks.count(char_after_word) > 0):
              word_found = True
          elif (char_before_word == ' '):
            if (char_after_word == ' '):              
              word_found = True
            elif (punctuation_marks.count(char_after_word) > 0):
              word_found = True
            else:              
              if (char_after_word == 's'):
                char_after_word_index = word_index + len(word_to_find)
                char_after_s = censored_line[char_after_word_index + 1]
                if (char_after_s == ' ' or punctuation_marks.count(char_after_s) > 0):
                  word_found = True
          elif (punctuation_marks.count(char_before_word) > 0):
            if (char_after_word == ' '):
              word_found = True
            elif (punctuation_marks.count(char_after_word) > 0):
              word_found = True

          if (word_found == True):
            new_line = censored_line[:word_index] + censored + censored_line[word_index + len(word):]
            censored_line = new_line           
          else:
            replacement_word = word[0] + '>' + word[1:]
            new_line = censored_line[:word_index] + replacement_word + censored_line[word_index + len(word_to_find) :]
            #new_line = censored_line.replace(word_to_find, replacement_word)
            censored_line = new_line
        replacement_word = word[0] + '>' + word[1:]
        if (censored_line.find(replacement_word) > -1):
         censored_line = censored_line.replace(replacement_word, word)
      censored_text_lines.append(censored_line)

#  for i in range(len(censored_text_lines)):
#    if (i == 0):
#      censored_text += censored_text_lines[i]
#    else:
#      censored_text += '\n' + censored_text_lines[i]
  censored_text = '\n'.join(censored_text_lines)
  return censored_text

def censor_multiple(text, word_list):
  censored_text = text
  for word in word_list:
    new_text = censor_text(censored_text, word)
    censored_text = new_text
  return censored_text

def censor_negativity(text, proprietary_terms, negative_words, censor_amount = 2):
  # censor_amount determines how many negative words need to be censored
  # censor_amount = 0: All negative words are to be censored
  # censor_amount = 1: All negative words that occur after the first negative word are to be censored
  # censor_amount = 2: All negative words that occur after the first two negative words are to be censored
  # 3, 4, etc.
  censored_text = censor_multiple(text, proprietary_terms)
  negative_word_indicies = []
  adjusted_start_index = 0
  for n_word in negative_words:
    if (censored_text.find(n_word) > -1):
      negative_word_indicies.append(censored_text.find(n_word))
    if (censored_text.find(n_word.title()) > -1):
      negative_word_indicies.append(censored_text.find(n_word.title()))
    if (censored_text.find(n_word.upper()) > -1):
      negative_word_indicies.append(censored_text.find(n_word.upper()))
  if (len(negative_word_indicies) > censor_amount):
    negative_word_indicies.sort()
    adjusted_start_index = negative_word_indicies[censor_amount]
  adjusted_text = censored_text[:adjusted_start_index]
  censored_text = censored_text[adjusted_start_index:]
  for n_word in negative_words:
    new_text = censor_text(censored_text, n_word)
    censored_text = new_text
  censored_text = adjusted_text + censored_text
  return censored_text

def censor_all(text, proprietary_terms, negative_words):  
  censored_text = ""
  censored_text_lines = []
  punctuation_marks = ['.', ',', '(', ')', '!', '?', '\'', '\"', ':', ';', '/']
  adjusted_text = censor_negativity(text, proprietary_terms, negative_words, 0)
  
  print(adjusted_text)
  adjusted_text_lines = adjusted_text.split('\n')
  for line in adjusted_text_lines:
    censored_line = ""
    line_words = line.split(' ')
    censored_words = line.split(' ')
    for i in range(len(line_words)):
      word = line_words[i]
      if (word.count('*') >= 1):        
        if (i == 0):
          next_word = line_words[i + 1]
          censored = ""
          for letter in next_word:
            if (punctuation_marks.count(letter) > 0):
              censored += letter
            else:
              censored += "*"          
          censored_words[i + 1] = censored
        elif (i == len(line_words) - 1):
          previous_word = line_words[i - 1]
          censored = ""
          for letter in previous_word:
            if (punctuation_marks.count(letter) > 0):
              censored += letter
            else:
              censored += "*"          
          censored_words[i - 1] = censored
        else:
          next_word = line_words[i + 1]
          censored = ""
          for letter in next_word:
            if (punctuation_marks.count(letter) > 0):
              censored += letter
            else:
              censored += "*"          
          censored_words[i + 1] = censored

          previous_word = line_words[i - 1]
          censored = ""
          for letter in previous_word:
            if (punctuation_marks.count(letter) > 0):
              censored += letter
            else:
              censored += "*"          
          censored_words[i - 1] = censored
    
    censored_line = ' '.join(censored_words)
    censored_text_lines.append(censored_line)

  censored_text = '\n'.join(censored_text_lines)  
  return censored_text

#test_censor = censor_text(test_text, "learning algorithms")
#email_one_censored = censor_text(email_one, 'learning algorithms')
#email_two_censored = censor_multiple(email_two, proprietary_terms)
#email_three_censored = censor_negativity(email_three, proprietary_terms, negative_words)
email_four_censored = censor_all(email_four, proprietary_terms, negative_words)
print(email_four_censored)

