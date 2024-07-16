from pgsync import plugin


class FullnamePlugin(plugin.Plugin):
    name = 'Fullname'

    def transform(self, doc, **kwargs):

        firstname = doc['firstName']
        lastname = doc['lastName']
        doc['fullname'] = f'{firstname}{lastname}'

        return doc
