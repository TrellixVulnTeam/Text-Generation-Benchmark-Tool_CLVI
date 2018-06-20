from summarizer_library import sumyKeys as SUMY_KEYS
import logging

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT,
                    level=logging.DEBUG)
LOGGER = logging.getLogger()


class SummarizerSwitch(object):
    def __init__(self, benchmarkInstance):
        self.benchmark = benchmarkInstance
        self.summarizer_library = benchmarkInstance.summarizer_library

        sumyKeys = SUMY_KEYS
        sumyFunctionMap = {k: self.sumySwap(k) for k in sumyKeys}

        self.functionMap = {
            'smmrre': self.smmrre,
            'sedona': self.sedona,
            'recollect': self.recollect
        }

        self.functionMap.update(sumyFunctionMap)

    def joinTokenizedSentences(self, text):
        benchmark = self.benchmark
        sentenceSeperator = benchmark.sentenceSeperator
        newText = text.replace(sentenceSeperator, '')
        return newText

    def splitTokenizedSentences(self, text):
        benchmark = self.benchmark
        sentenceSeperator = benchmark.sentenceSeperator
        newText = text.split(sentenceSeperator)
        return newText

    def toggleAndExecuteSummarizer(self, summarizerKey, text):
        functions = self.functionMap

        if summarizerKey in functions:
            summary = None
            try:
                method = functions[summarizerKey]
                # Method should return a summary
                summary = method(text)
            except Exception as err:
                # Failed summariesare logged so they can be investigated.
                LOGGER.error(str(err))

            return summary

        error = '{0}: Is not an available summarizer'.format(summarizerKey)
        raise ValueError(error)

    def recollect(self, text):
        benchmark = self.benchmark
        numSentences = benchmark.sentenceCount

        if benchmark.preTokenized:
            # smmrRE expects text to not be pretokenized
            text = self.joinTokenizedSentences(text)

        RecollectClass = self.summarizer_library['recollect']
        LANGUAGE = 'en'
        recollect = RecollectClass(LANGUAGE)

        summary = recollect.summarize(text, numSentences)

        return summary

    def sedona(self, text):
        benchmark = self.benchmark
        numSentences = benchmark.sentenceCount

        if benchmark.preTokenized:
            # smmrRE expects text to not be pretokenized
            text = self.joinTokenizedSentences(text)

        SedonaClass = self.summarizer_library['sedona']
        sedona = SedonaClass()

        summary = sedona.summarize(text, numSentences)

        return summary

    def smmrre(self, text):
        benchmark = self.benchmark
        numSentences = benchmark.sentenceCount

        if benchmark.preTokenized:
            # smmrRE expects text to not be pretokenized
            text = self.joinTokenizedSentences(text)

        smmrREClass = self.summarizer_library['smmrre']
        smmrRE = smmrREClass(text)

        summary = smmrRE.summarize(numSentences)

        return summary

    def sumySwap(self, sumyMethodKey):
        def sumyFunc(text):
            benchmark = self.benchmark
            numSentences = benchmark.sentenceCount

            if benchmark.preTokenized:
                # sumy has it's own tokenizer
                text = self.joinTokenizedSentences(text)

            summarizer = self.summarizer_library[sumyMethodKey]
            summary = summarizer(text, numSentences, 'english')

            return summary
        return sumyFunc
