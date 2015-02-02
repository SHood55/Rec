package com.company;

import com.gc.android.market.api.MarketSession;
import com.gc.android.market.api.model.Market;

public class Main {

    public static void main(String[] args) {
	// write your code here

        String email = "wilhelmws@gmail.com";
        String password = "1.9.Alpha";
        MarketSession session = new MarketSession();
        session.login(email, password);
//        session.getContext.setAndroidId(myAndroidId);

        String query = "games";
        Market.AppsRequest appsRequest = Market.AppsRequest.newBuilder()
                .setQuery(query)
                .setStartIndex(0).setEntriesCount(10)
                .setWithExtendedInfo(true)
                .build();

        session.append(appsRequest, new MarketSession.Callback<Market.AppsResponse>() {
            @Override
            public void onResult(Market.ResponseContext context, Market.AppsResponse response) {
                // see AppsResponse class definition for more infos

                printRespones(response);
            }
        });
        session.flush();

    }
    public static void printRespones(Market.AppsResponse response){
        for (int i = 0; i < response.getAppCount(); i++) {
            printApp(response.getApp(i));

        }
    }
    public static void printApp(Market.App app){
            System.out.println("Title: " + app.getTitle() + ", appType: " + app.getAppType() + ", creator: " + app.getCreator());

    }

}
