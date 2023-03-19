

from ProjectInstanceGenerator.AMMMGlobals import AMMMException


class ValidateConfig(object):
    # Validate config attributes read from a DAT file.

    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        paramList = ['instancesDirectory', 'fileNamePrefix', 'fileNameExtension', 'numInstances',
                      'n', 'm', 'e', 'f' ]
        for paramName in paramList:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter(%s) has not been not specified in Configuration' % str(paramName))

        instancesDirectory = data.instancesDirectory
        if len(instancesDirectory) == 0: raise AMMMException('Value for instancesDirectory is empty')

        fileNamePrefix = data.fileNamePrefix
        if len(fileNamePrefix) == 0: raise AMMMException('Value for fileNamePrefix is empty')

        fileNameExtension = data.fileNameExtension
        if len(fileNameExtension) == 0: raise AMMMException('Value for fileNameExtension is empty')

        numInstances = data.numInstances
        if not isinstance(numInstances, int) or (numInstances <= 0):
            raise AMMMException('numInstances(%s) has to be a positive integer value.' % str(numInstances))

        n = data.n
        if not isinstance(n, int) or (n <= 0):
            raise AMMMException('n(%s) has to be a positive integer value.' % str(n))

        m = data.m
        if not isinstance(m, int) or (m <= 0):
            raise AMMMException('m(%s) has to be a positive integer value.' % str(m))


        e = data.e
        if not isinstance(e, int) or (e <= 0):
            raise AMMMException('e(%s) has to be a positive integer value.' % str(e))

        f = data.f
        if not isinstance(f, int) or (f <= 0):
            raise AMMMException('f(%s) has to be a positive integer value.' % str(f))
