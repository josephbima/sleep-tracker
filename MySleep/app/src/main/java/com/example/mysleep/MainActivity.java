package com.example.mysleep;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Switch;
import android.widget.TextView;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity implements SensorEventListener {
    float x_value, y_value, z_value;
    ArrayList<String> data_array = new ArrayList<String>();
    TextView x_view, y_view, z_view;
    Button btn;
    Switch switchAccelerometer;

    SensorManager sensor_manager;
    Sensor acc_sensor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        x_view = (TextView) findViewById(R.id.x_val);
        y_view = (TextView) findViewById(R.id.y_val);
        z_view = (TextView) findViewById(R.id.z_val);
        btn = (Button) findViewById(R.id.summaryButton);
        switchAccelerometer = (Switch) findViewById(R.id.accelerometerSwitch);

        sensor_manager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        if (sensor_manager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) != null){
            acc_sensor = sensor_manager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
            sensor_manager.registerListener(this, acc_sensor, SensorManager.SENSOR_DELAY_NORMAL);
        }
        else{
            Log.v("Failed", "Cannot get the sensor");
        }
        switchAccelerometer.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    write_data(data_array);

                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    protected void onResume(){
        super.onResume();
        sensor_manager.registerListener(this, acc_sensor, SensorManager.SENSOR_DELAY_NORMAL);
    }

    protected void onPause(){
        super.onPause();
        sensor_manager.unregisterListener(this);
    }


    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy){

    }

    @Override
    public void onSensorChanged(SensorEvent event){
        x_value = event.values[0];
        y_value = event.values[1];
        z_value = event.values[2];
        x_view.setText(Float.toString(x_value));
        y_view.setText(Float.toString(y_value));
        z_view.setText(Float.toString(z_value));
        data_array.add(Float.toString(x_value) + " " + Float.toString(y_value) + " " + Float.toString(z_value) + "\n");
    }
    public void write_data(ArrayList<String> data) throws IOException {
        File file = getFileStreamPath("data.txt");
        if(!file.exists()){
            file.createNewFile();
        }
        FileOutputStream writer = openFileOutput(file.getName(), Context.MODE_PRIVATE);
        for (String string: data){
            writer.write(string.getBytes());
            writer.flush();
        }
        writer.close();
    }
}
