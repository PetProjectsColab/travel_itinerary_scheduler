package com.example.android.visualpolish;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;



public class SignUpActivity extends AppCompatActivity {
    String email;
    String name;
    String password;
    String re_password;
    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.sign_up);

        final EditText mEmail = (EditText) this.findViewById(R.id.su_email);
        final EditText mUsername = (EditText) this.findViewById(R.id.su_username);
        final EditText mPassword = (EditText) this.findViewById(R.id.su_password);
        final EditText mRePassword = (EditText) this.findViewById(R.id.su_re_password);

        final Button mSignUp = (Button) this.findViewById(R.id.su_sign_up);

        mSignUp.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                email = mEmail.getText().toString();
                name = mUsername.getText().toString();
                password = mPassword.getText().toString();
                re_password = mRePassword.getText().toString();
                if(!email.isEmpty() && !name.isEmpty() && !password.isEmpty() && !re_password.isEmpty()){
                    if(!password.equals(re_password)){
                        Toast.makeText(getApplicationContext(),
                                "-Passwords don't match!", Toast.LENGTH_LONG)
                                .show();
                    }
                }
            }
        });


        //mUsername = (TextView) findViewById(R.id.si_username);

    }
}
