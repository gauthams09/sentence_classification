from os import path
from glob import glob
from xml.etree import ElementTree

class ReadDatasetException(Exception):
    """Base class for exceptions."""

class DirectoryNotFoundException(ReadDatasetException):
    """Raised when dataset directory is not found."""

class NoFilesFoundException(ReadDatasetException):
    """Raised when no files were found in dataset directory."""

class DatasetParseException(ReadDatasetException):
    """Raised when dataset couldnt be parsed as valid xml."""

class DataFetchException(ReadDatasetException):
    """Raised when field or data couldnt be fetched from parsed dataset."""

def read_dataset(dataset_dir):
    '''
    Reads the datasets from the directory.

    Args:
        dataset_dir (str): Path to dataset directory.

    Returns:
        datasets (list): The datasets read from directory.

    Raises:
        DirectoryNotFoundException : Directory not found
        NoFilesFoundException : No files matching filename pattern found in directory
        DatasetParseException : Couldnt parse the dataset file with xml parser
        DataFetchException : Couldnt fetch field from dataset object



    '''
    datasets = []
    if not path.exists(dataset_dir):
        raise DirectoryNotFoundException(DirectoryNotFoundException, 'Dataset directory not found at {}'.format(dataset_dir))
    for file in glob(path.join(dataset_dir, '*.xml')):
        try:
            tree = ElementTree.parse(file)
        except Exception as e:
            raise DatasetParseException(DatasetParseException, e)
        root = tree.getroot()
        data_dict = {}
        data_dict['question'] = {}
        try:
            data_dict['question']['id'] = root.attrib['id'].lower()
            for first_child in root.getchildren():
                if first_child.tag == "questionText":
                    data_dict['question']['text'] = first_child.text
                elif first_child.tag == "referenceAnswers":
                    reference_answer = first_child.getchildren()[0]
                    data_dict['reference_answer'] = {
                            'id' : reference_answer.attrib['id'],
                            'text' : reference_answer.text
                            }
                elif first_child.tag == "studentAnswers":
                    data_dict['answers'] = {'sentences' : [], 'classes' : []}
                    for answer in first_child.getchildren():
                        data_dict['answers']['sentences'].append(answer.text)
                        data_dict['answers']['classes'].append(answer.attrib['accuracy'])
                else:
                    pass
        except Exception as e:
            raise DataFetchException(DataFetchException, e)
        datasets.append(data_dict)
    if len(datasets) == 0:
        raise NoFilesFoundException(NoFilesFoundException, 'No dataset files found at {}'.format(dataset_dir))
    return datasets
