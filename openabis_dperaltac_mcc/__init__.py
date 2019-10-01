import os

from cffi import FFI

TEMPLATE_FORMAT_ISO19794 = "iso19794"
TEMPLATE_FORMAT_XYT = "xyt"


class DPeraltacMCC:
    """
    Performs matching procedure based on operating point and template format that is used in the process

    :param fnmr: False non-matching rate level
    :param input_format: Format of the input templates
    """

    def __init__(self, config):
        self.input_format = TEMPLATE_FORMAT_ISO19794
        self.ffi = FFI()
        self.ffi.cdef(
            """
            float match_iso_buffer(char * arg1, char * arg2);
            float match_xyt_buffer(char * arg1, char * arg2);
            """
        )
        self.mcc = self.ffi.dlopen(os.path.join(os.path.dirname(os.path.realpath(__file__)), "py_mcc.so"))

    def match_fingerprints(self, fingerprint1, fingerprint2):
        template1 = self.get_template(fingerprint1)
        template2 = self.get_template(fingerprint2)

        return self.match_templates(template1, template2)

    def get_template(self, fingerprint):
        for template in fingerprint.templates:
            if template.format == self.input_format:
                return template.template
        return None

    def match_templates(self, fingerprint1, fingerprint2):
        """
        Match two buffers.
        Two options of buffers: ISO-19794 template buffer or xyt buffer.

        :param fingerprint1: Buffer in xyt format (X, Y, T, Q) or iso format
        :param fingerprint2: Buffer in xyt format (X, Y, T, Q) or iso format

        :return score: Score of the matching procedure
        """
        if self.input_format == TEMPLATE_FORMAT_ISO19794:
            score = self.mcc.match_iso_buffer(fingerprint1, fingerprint2)
        elif self.input_format == TEMPLATE_FORMAT_XYT:
            str1 = fingerprint1.replace("\n", ".")
            str2 = fingerprint2.replace("\n", ".")
            score = self.mcc.match_xyt_buffer(str1.encode("ascii"), str2.encode("ascii"))
        else:
            raise Exception("Unknown format for matching. Aborting...")
        return score
