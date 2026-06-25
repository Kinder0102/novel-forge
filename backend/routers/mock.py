import json
from fastapi import APIRouter, Request

from services.ai_service.mock_data import MOCK_CHAPTER_CONTENT

router = APIRouter()

MOCK_DATA = {
    "worldbuilding": {
        "title": "奇幻世界",
        "genre": "奇幻",
        "description": "這是一個名為「奇幻」的奇幻世界，充滿魔法與冒險。大陸上有五大王國，各自擁有獨特的文化與力量體系。古老的預言預示著一位天命之人的降臨，將為這片土地帶來前所未有的變革。各地的種族——人類、精靈、矮人、獸人——在脆弱的和約下共存，但暗處的勢力正蠢蠢欲動。",
        "setting": "故事發生在中土大陸，這片土地經歷了千年的戰火與和平交替。北方的冰封山脈、東方的迷霧森林、南方的沙漠帝國、西方的海洋群島，構成了一幅壯麗的地理畫卷。當前時代處於「龍息紀元」的尾聲，魔法正在逐漸消退。",
        "rules": "魔法分為五大元素體系——風、火、水、土、光，每種元素需天賦契合者才能駕馭。元素之力消耗生命力，過度使用會加速衰老甚至死亡。大陸上「元素守護者」以維持平衡為使命，而「暗影之主」則試圖聚合五大元素之力改寫世界法則。古老的預言規定，唯有五大元素的繼承者齊聚黎明之塔，才能阻止暗影吞噬大地。",
    },
    "character": {
        "name": "艾莉絲·風行者",
        "role": "主角",
        "personality": "勇敢果斷、正義感強烈，內心深處卻藏著對過去的傷痛。她總是先行動再思考，這既是她的優點也是致命傷。對朋友忠誠，對敵人毫不留情，但在面對道德抉擇時會陷入掙扎。",
        "background": "艾莉絲出生於邊境小鎮，幼年時目睹家園被暗影軍團摧毀，父母雙亡。她被一位退役的老騎士收養，習得劍術與生存之道。十八歲那年，她意外發現自己擁有駕馭風元素的天賦，從此踏上尋找真相的旅程。",
        "appearance": "銀白色長髮及腰，平時束成俐落的高馬尾。淺藍色眼眸在發動風元素之力時會泛起微光。身形纖瘦但結實，常年穿著深褐色皮甲和旅行斗篷，腰間掛著一把樸素的長劍。左前臂有一道從廢墟中留下的淺淡疤痕。",
    },
    "outline": {
        "title": "風之軌跡",
        "description": "少女艾莉絲在失去家園後，踏上了尋找真相與復仇的旅程。一路上她結識了形形色色的同伴，揭開了暗影軍團背後更大陰謀的面紗。這是一個關於成長、犧牲與希望的故事——當世界的命運落在一個年輕女孩肩上時，她必須在仇恨與寬恕之間做出最終選擇。",
        "chapters": [
            {"title": "第一章　餘燼中的風", "summary": "艾莉絲在廢墟中醒來，目睹家園被暗影軍團摧毀的慘狀。她在瓦礫中找到母親留給她的風之吊墜，決定踏上旅程。途中遇到一位神秘老巫師，留下一句晦澀的預言後消失——「風之繼承者將在黎明之塔喚醒沉睡的光」。艾莉絲帶著困惑與決心，走向迷霧森林。"},
        ],
    },
    "scene": [
        {"scene_number": 1.0, "title": "廢墟中的風", "description": "艾莉絲從昏迷中醒來，四周滿是焦黑的瓦礫。她顫抖著站起來，在廢墟中翻找，找到了母親的風之吊墜。風在她指尖輕柔地流轉，像是母親最後的撫摸。"},
        {"scene_number": 2.0, "title": "老者的預言", "description": "在通往北方的土路上，一位身著灰袍的老者攔住了艾莉絲。他眼中閃爍著不屬於凡人的光芒，說出了關於「風之繼承者」和「黎明之塔」的預言，然後化作一陣煙霧消失。"},
        {"scene_number": 3.0, "title": "踏上征途", "description": "夕陽西下，艾莉絲站在岔路口，向北是迷霧森林，向南是繁華的王都。她握緊吊墜，毅然轉身向北。遠方森林的邊緣，一雙精靈的眼睛正在暗處注視著她的身影。"},
        {"scene_number": 4.0, "title": "暴風雨之夜", "description": "入夜後突如其來的暴風雨迫使艾莉絲躲進一個廢棄山洞。在洞中，牆上的古老壁畫訴說著元素守護者的傳說。她發覺吊墜在黑暗中發出微弱的藍光，似乎在回應著什麼。"},
    ],
    "chapter": MOCK_CHAPTER_CONTENT,
    "compact": "mock compact summary",
}


@router.post("/chat/completions")
async def mock_chat_completion(request: Request):
    body = await request.json()
    model = body.get("model", "")
    module_name = model.removeprefix("mock-") if model.startswith("mock-") else model

    data = MOCK_DATA.get(module_name)
    if data is None:
        content = json.dumps({"error": f"unknown module: {module_name}"}, ensure_ascii=False)
    else:
        content = data if isinstance(data, str) else json.dumps(data, ensure_ascii=False)

    return {
        "choices": [{"message": {"content": content}}],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }
