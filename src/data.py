import json
class Data:
    def __init__(self, json_file):
        self.json_file = json_file
        self.data = self.json()

    def array_on_duplicate_keys(ordered_pairs):
        """Convert duplicate keys to arrays."""
        d = {}
        for k, v in ordered_pairs:
            if k in d:
                if type(d[k]) is list:
                    d[k].append(v)
                else:
                    d[k] = [d[k],v]
            else:
                d[k] = v
        return d

    # get json data from file
    def json(self):
        
        with open(self.json_file, 'r') as f:
            try:
                return json.load(f, object_pairs_hook=Data.array_on_duplicate_keys)
            except json.decoder.JSONDecodeError:
                return None
    
    # get data
    def get(self, key):
        return self.data[key]
    
    # get AssayResults
    def get_assay_results(self):
        try:
            return self.data['QuantitativeResponseAssay']['AssayResults']
        except KeyError:
            return None
    
    def get_template (self):
        try:
            return self.data['QuantitativeResponseAssay']['Meta']['Template']['Key']
        except KeyError:
            return None
    
    def get_date(self):
        try:
            return self.data['QuantitativeResponseAssay']['Meta']['Creation']['Time'].split('T')[0]
        except KeyError:
            return None
    
    # get AssayResult
    def get_assay_result(self, index):
        try:
            return self.get_assay_results()[index]
        except KeyError:
            return None
    
    def values_from_json(self):
        counter = 1

        while True:
            key = f'AssayResult[{counter}]'
            try:
                if key in self.get_assay_results():
                    second_counter = 1
                    while True:
                        second_key= f'ParameterEstimate[{second_counter}]'
                        if second_key in self.get_assay_result(key)['FullModel']['FitResult']:
                            full_model = self.get_assay_result(key)['FullModel']['FitResult'][second_key]
                            parameter_name = full_model['ParameterName']
                            assay_element_name = full_model['AssayElementName']
                            parameter_value = full_model['Value']
                            if assay_element_name != None:
                                if 'Position' in assay_element_name:
                                    assay_element_name = assay_element_name.split(' ')[1]
                                    yield assay_element_name, parameter_name, parameter_value
                            second_counter += 1
                        else:
                            break
                    
                    counter += 1
                else:
                    break
            except TypeError:
                yield None, None, None
                break
    
    def get_values(self):
        mydict = {}
        for pos, param, value in self.values_from_json():
            if pos not in mydict:
                mydict[pos] = {}

            mydict[pos][param] = value

        return mydict
    


if __name__ == '__main__':
    data = Data('data/2019/318A-0010823_Assay_Replicate_1 2022-04-28T07_24_50Z.json')
    mydict = data.get_values()



    for pos in mydict:
        print(pos, mydict[pos])
        