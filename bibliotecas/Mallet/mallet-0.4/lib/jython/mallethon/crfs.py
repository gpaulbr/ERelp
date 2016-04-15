"""
import statements. 
"""
from edu.umass.cs.mallet.base.types import InstanceList
from edu.umass.cs.mallet.base.fst import CRF4
from edu.umass.cs.mallet.base.pipe.iterator import LineGroupIterator
from edu.umass.cs.mallet.base.pipe import SimpleTaggerSentence2TokenSequence
from edu.umass.cs.mallet.base.pipe import SerialPipes, Pipe
from java.util.regex import Pattern
from java.io import FileReader, File, ObjectOutputStream, FileOutputStream
from java.io import FileInputStream, ObjectInputStream
from java.lang import Double
import jarray

"""
make a serial pipe from a python sequence of pipes.  The first element in the
pipe should pipe instances with data of the type given by the InstanceList that
will be added and produce a TokenSequence, intermediates should take and
produce Instances with data of type TokenSequence and the final one should take
instances of type TokenSequence and produce instance with data of type
FeatureVectorSequence.
"""
def List2Pipe(pipeSequence, defaultLabel):
    p=SerialPipes(jarray.array(pipeSequence, Pipe))
    p.getTargetAlphabet().lookupIndex(defaultLabel)
    return p

"""
Takes a pipe and a file name and produces an instance list based on that pipe
and a LineGroupIterator.  The optional argument seperator specifies what
seperates instances from eachother.  For example, when doing part of speech
tagging an instance is a sentence.  Each word in the sentence would have a
seperate line and a line matching the regular expression specified by seperator
would terminate the current sentence. 
"""
def LineGroupInstanceList(pipe, fileName, seperator="^\\s*$"):
    data = InstanceList(pipe)
    data.add(LineGroupIterator(FileReader(File(fileName)),
		               Pattern.compile(seperator), 
			       1))
    return data

"""
add some extra data to an instance list. 
"""
def LineGroupInstanceAdd(data,fileName, seperator="^\\s*$"):
    data.add(LineGroupIterator(FileReader(File(fileName)),
		Pattern.compile(seperator),
		1))

"""
Create and initialize a CRF with states read from data, of order given by the
sequence orderList (lower numbers are backoff levels), and a default label and
with gaussian prior variance as given.  The allowedPattern, forbiddenPattern
and connected control what state transitions are permissible.  Allowed
transitions (from LABEL1 to LABEL2) are ones where "LABEL1,LABEL2" match the
allowedPattern but not the forbiddenPattern.  For example:

forbiddenPattern="O,I-.*"

would disallow transitions from state "O" to state "I-NP", "I-PP" and so on. 

allowedPattern="B-(.*),I-\\1|I-(.*),I-\\2|.*,B-.*|.*,O"

would allow e.g. B-NP,I-NP but not B-NP,I-VP.
"""
def initNewCRF(data, orderList, defaultLabel, gaussianPriorVariance, 
	allowedPattern=".*", forbiddenPattern="\\s", connected=1):
    # some default things that most users won't want to deal with  
    forbiddenPattern = Pattern.compile(forbiddenPattern)
    allowedPattern = Pattern.compile(allowedPattern)
    defaults = None
    orderArray = jarray.array(orderList,"i")
    crf = CRF4(data.getPipe(), None) 
    startName = crf.addOrderNStates(data, orderArray, defaults,
	    defaultLabel, forbiddenPattern, allowedPattern, connected);
    crf.setGaussianPriorVariance (gaussianPriorVariance);
    for i in range(0,crf.numStates()):
        crf.getState(i).setInitialCost(Double.POSITIVE_INFINITY)
    crf.getState(startName).setInitialCost(0.0);
    return crf

""" 
Save a CRF model to a file
""" 
def saveModel(crf, file):
    s=ObjectOutputStream(FileOutputStream(file))
    s.writeObject(crf);
    s.close();

""" 
Read a CRF model from a file
""" 
def loadModel(file):
    s = ObjectInputStream(FileInputStream(file))
    crf = s.readObject()
    s.close()
    return crf

"""
Print out helpful debugging information about data set.
"""
def printInstanceInfo (name, instanceList):
   print "Number of %s instances = %d" % (name, instanceList.size ()) 

"""
Print out the number of features and the value of the labels we found (so the
    user can do sanity checking).
"""
def printDataInfo(p):
#    print("Number of features in data: "+ p.getDataAlphabet().size().toString())
    print "Number of features in data = %d" % p.getDataAlphabet().size()
    targets = p.getTargetAlphabet();
    buf = "Labels:"
    for i in range(0,targets.size()):
      buf+=" "+targets.lookupObject(i).encode()
    print buf


