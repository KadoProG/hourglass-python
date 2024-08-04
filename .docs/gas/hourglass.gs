// LINEBotのチャネルアクセストークン
const LINE_BOT_TOKEN = LINEBotのチャネルアクセストークン;
// LINE APIの基本となるURL
const LINE_BASE_URL = "https://api.line.me/v2/bot";
// LINEBotの認証ヘッダー
const HEADER = {
  "Content-Type": "application/json; charset=UTF-8",
  Authorization: "Bearer " + LINE_BOT_TOKEN,
};

const USER_ID = ユーザID;

function doGet() {
  var now = new Date();
  var formattedDateTime = Utilities.formatDate(
    now,
    Session.getScriptTimeZone(),
    "yyyy-MM-dd HH:mm:ss"
  );
  var message =
    "砂時計のタイマーが終了しました\n" + "現在の日時: " + formattedDateTime;

  sendLineMessage(USRE_ID, message);
}

function sendLineMessage(userId, message) {
  var url = LINE_BASE_URL + "/message/push";

  var postData = {
    to: userId,
    messages: [
      {
        type: "text",
        text: message,
      },
    ],
  };

  var options = {
    method: "post",
    headers: HEADER,
    payload: JSON.stringify(postData),
  };

  UrlFetchApp.fetch(url, options);
}
