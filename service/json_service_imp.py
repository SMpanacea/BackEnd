from service.json_service import Json_Service

class Json_Service_Imp(Json_Service):

    def json_key_check(self, json, key):  # json 통신 결과의 key가 존재하는지 확인하는 함수
        try:
            buf = json[key]
        except KeyError:    
            # key가 존재하지 않을 경우
            return False
        # key가 존재할 경우
        return True
    
    def check_image(self, request):
        image_files = request.files.getlist("image")
        if not image_files:
            return "false"
        else:
            return "true"