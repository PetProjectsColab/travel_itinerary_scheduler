package com.example.android.visualpolish;

import android.app.DownloadManager;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONObject;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import static android.R.attr.type;
import static java.net.Proxy.Type.HTTP;
//stay logged in

public class MainActivity extends AppCompatActivity {

    String name;
    String password;
    private ProgressDialog pDialog;
    private int flag_output=-1;

    private static final String m_hostname = "172.30.29.130";
    private static final int m_portNumber = 5000;
    private final String mSignUpAddress="/v1/signup";
    private final String mSignInAddress="/v1/login";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.sign_up_in);
        //setContentView(R.layout.activity_main);
        final EditText mUsername = (EditText) this.findViewById(R.id.si_username);
        final EditText mPassword = (EditText) this.findViewById(R.id.si_password);
        final Button mSignIn = (Button) this.findViewById(R.id.sign_in);
        final Button mSignUp = (Button) this.findViewById(R.id.sign_up);


        //mUsername = (TextView) findViewById(R.id.si_username);
        //Log.d("NAME",mUsername.getText().toString());
        //mUsername = (TextView) findViewById(R.id.si_password);
        //Log.d("PASSWORD",mPassword.getText().toString());
        //assert mUsername != null;
        //assert mPassword != null

        if(SaveSharedPreferences.getUserName(MainActivity.this).length() == 0)
        {
            // call Login Activity
            mSignIn.setOnClickListener(new View.OnClickListener() {
                public void onClick(View v) {
                    name = mUsername.getText().toString();
                    password = mPassword.getText().toString();

                    if (!name.isEmpty() && !password.isEmpty()) {
                        //new LoginRegister().execute();
                        Log.d("NAME", name);
                        //mUsername = (TextView) findViewById(R.id.si_password);
                        Log.d("PASSWORD", password);
                        new LoginRegister().execute();
                    } else {
                        //prompt user to enter credentials
                        Toast.makeText(getApplicationContext(),
                                "Please enter the credentials!", Toast.LENGTH_LONG)
                                .show();
                    }

                    //mUsername = (TextView) findViewById(R.id.si_username);

                    //Intent numbersIntent = new Intent(MainActivity.this, SignInActivity.class);

                    //startActivity(numbersIntent);
                }
            });
        }
        else
        {
            // Stay at the current activity.
        }



        mSignUp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                Intent intent = new Intent(MainActivity.this,
                        SignUpActivity.class);
                startActivity(intent);
                finish();
            }
        });
    }
        private class LoginRegister extends AsyncTask<Void, Void, Void> {

            @Override
            protected void onPreExecute() {
                super.onPreExecute();
                // Showing progress dialog
                pDialog = new ProgressDialog(MainActivity.this);
                pDialog.setMessage("Logging in...");
                pDialog.setCancelable(false);
                pDialog.show();

            }


            @Override
            protected Void doInBackground(Void... arg0) {
                    // Create a new HttpClient and Post Header
                    HttpClient httpclient = new DefaultHttpClient();
                    HttpPost httppost = new HttpPost("http://"+m_hostname+":"+m_portNumber+mSignInAddress);

                    Log.d("URL","http://"+m_hostname+":"+m_portNumber+mSignInAddress);
                    String responseBody = "";

                    HttpResponse response = null;

                    try {

                        String base64EncodedCredentials = "Basic " + Base64.encodeToString(
                                (name + ":" + password).getBytes(),
                                Base64.NO_WRAP);


                        Log.d("base",base64EncodedCredentials);
                        httppost.setHeader("Authorization", base64EncodedCredentials);

                        httppost.setHeader("Content-Type","application/json");

                        // Execute HTTP Post Request
                        response = httpclient.execute(httppost);
                        Log.d("HTTP","Before Response");

                        if (response.getStatusLine().getStatusCode() == 200) {
                            Log.d("response ok", "ok response :/");
                            flag_output=1;
                        } else {
                            Log.d("response not ok", "Something went wrong :/");
                        }

                        responseBody = EntityUtils.toString(response.getEntity());

                    }
                    catch (IOException e){
                        e.printStackTrace();
                    }



                    //return responseBody;

                return null;
            }

            @Override
            protected void onPostExecute(Void result) {
                super.onPostExecute(result);
                // Dismiss the progress dialog
                if (pDialog.isShowing())
                    pDialog.dismiss();

                //if login fails show pop-up
                if (flag_output == -1) {
                    Toast.makeText(getApplicationContext(),
                            "-Login Failed!", Toast.LENGTH_LONG)
                            .show();
                } else {
                    // Launch main activity and send session_ctom to products activity
                    //Log.e(TAG, "Launching main activity.");
                    Intent intent = new Intent(MainActivity.this,
                            SignInActivity.class);
                    startActivity(intent);
                    finish();
                }
            }
        }
}

