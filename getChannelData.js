function getChannelData() {
    // APIキー
    var key = ""
    var sheetName = "liver_info_line"
  
    var ss = SpreadsheetApp.getActiveSpreadsheet() // アクティブなスプレットシートの取得
    var srcSheet = ss.getSheetByName(sheetName);
  
    var row_title = 1;
    var row_url = 2;
    var row_subscribe = 3;
    var row_view = 4;
    var row_video = 5;
    var row_thumbnails = 6;
    var colStart = 2;
    var colEnd = srcSheet.getDataRange().getLastColumn();
  
    // 各列ごとに処理
    for (i=colStart; i<=colEnd; i++) {
        // チャンネルをセット
        var channelURL = srcSheet.getRange(row_url, i).getValue();
        var channelID = channelURL.slice(32); // なんで？

        // 各種データのURL生成
        var channels_snippet_url = "https://www.googleapis.com/youtube/v3/channels?part=snippet&id=" + channelID +"&key=" + key ;
        var channels_statistics_url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + channelID +"&key=" + key;

        // 各種データ取得
        var channels_snippet_response = UrlFetchApp.fetch(channels_snippet_url);
        var channels_statistics_response = UrlFetchApp.fetch(channels_statistics_url);

        // チャンネルタイトルを抽出
        var channelTitle = JSON.parse(channels_snippet_response.getContentText()).items[0].snippet.title;
        
        // 登録者数を取得
        var subscribe_cnt = JSON.parse(channels_statistics_response.getContentText()).items[0].statistics.subscriberCount;

        // 総閲覧数を取得
        var view_cnt = JSON.parse(channels_statistics_response.getContentText()).items[0].statistics.viewCount;

        // サムネイル画像URLを取得
        var thumbnails_url = JSON.parse(channels_snippet_response.getContentText()).items[0].snippet.thumbnails.default.url; //古いランタイムではエラーがでる

        // チャンネルタイトルをシートに挿入
        srcSheet.getRange(row_title, i).setValue(channelTitle);

        // 登録者数をシートに挿入
        srcSheet.getRange(row_subscribe, i).setValue("登録者数");
        srcSheet.getRange(row_subscribe, i).setValue(subscribe_cnt);

        //総再生回数をシートに挿入
        srcSheet.getRange(row_view,1).setValue("総閲覧数");
        srcSheet.getRange(row_view,i).setValue(view_cnt);

        //動画数をシートに挿入
        srcSheet.getRange(row_video,1).setValue("アップロード動画数");
        srcSheet.getRange(row_video,i).setValue(video_cnt);

        //サムネイル画像URLをシートに挿入
        srcSheet.getRange(row_thumbnails_url,1).setValue("サムネイル画像URL");
        srcSheet.getRange(row_thumbnails_url,i).setValue(thumbnails_url);
    }
};
