from time import sleep
from googletrans import Translator
import backoff

class TranslatorNew:
    def __init__(self):
        self.client = Translator()
        self.sleep_in_between_translations_seconds = 1
        self.source_language = "en"
        self.max_chunk_size = 4000

    def __createChunks(self, corpus):
        chunks = [corpus[i:i + self.max_chunk_size] for i in range(0, len(corpus), self.max_chunk_size)]
        return chunks

    def __sleepBetweenQuery(self):
#         print('Sleeping for {}s after translation query..'.format(self.sleep_in_between_translations_seconds))
        sleep(self.sleep_in_between_translations_seconds)

    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    def Translate(self, content, dest_language_code):
        try:
#             print('Attempting to translate to lang={}'.format(dest_language_code))
            if len(content) > self.max_chunk_size:
                print('Warning: Content is longer than allowed size of {}, breaking into chunks'.format(self.max_chunk_size))
                results_list = []
                concatenated_result = ""

                original_chunks = self.__createChunks(content)
                for i in original_chunks:
                    r = self.client.translate(i, dest=dest_language_code, src=self.source_language)
                    self.__sleepBetweenQuery()
                    results_list.append(r.text)

                for i in results_list:
                    concatenated_result += i

                return concatenated_result
            else:
                res = self.client.translate(content, dest=dest_language_code, src=self.source_language)
                self.__sleepBetweenQuery()
                return res.text
        except Exception as e:
            print(e)
            raise e