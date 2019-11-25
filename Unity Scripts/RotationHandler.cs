using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//RotationHandler is attached to a camera component. It rotates as the camera
//as it takes screenshots of the given objects in the Resources folder.

public class RotationHandler : MonoBehaviour
{
	public GameObject obj;

    public static GameObject[] myObjects;

	public float distance;
	public int quarter_arc_count;
	public int level_circle_count;

	public bool take_screenshot;

	private float time_counter;
	private float around_y_rotation;
	private float arc_x_increment;

	private int level_ss_counter = 0;
	private int init_position_counter = 0;
	private int object_counter = 0;

	private string ss_name;

	private bool keep_going = true;
	Vector3[] startingPositions;

	GameObject myObj;
    // Start is called before the first frame update
    void Start()
    {
    	myObjects = Resources.LoadAll<GameObject>("");

    	startingPositions = new Vector3[quarter_arc_count];

    	around_y_rotation = 360/level_circle_count;
    	arc_x_increment = distance/(quarter_arc_count + 1);

    	for (int i = 0; i < quarter_arc_count; i++){

    		startingPositions[i] = new Vector3(arc_x_increment*(i+1), Mathf.Sqrt(Mathf.Pow(distance,2) - Mathf.Pow(arc_x_increment*(i+1), 2)), 0);
    	}


    	transform.position = startingPositions[init_position_counter];
		transform.LookAt(obj.transform.position);
		init_position_counter += 1;

		myObj = Instantiate(myObjects[object_counter]) as GameObject;
		object_counter += 1;
		init_position_counter = 0;

    }

    // Update is called once per frame
    void Update()
    {
    	if(keep_going){
    		time_counter += Time.deltaTime;
    	}

    	if(time_counter >= 0.1 && object_counter <= myObjects.Length){

    		if(init_position_counter < quarter_arc_count){
	    		if(level_ss_counter < level_circle_count){
	    			transform.RotateAround(new Vector3(obj.transform.position.x, 0, 0), Vector3.up, around_y_rotation);
	    			level_ss_counter +=1 ;
	    		}

	    		else{
	    			transform.position = startingPositions[init_position_counter];
	    			transform.LookAt(obj.transform.position);
	    			level_ss_counter = 0;
	    			init_position_counter += 1;
	    		}
	    	}

	    	else{
	    		Destroy(myObj);
	    		myObj = Instantiate(myObjects[object_counter]) as GameObject;
	    		object_counter += 1;
	    		init_position_counter = 0;


		    	transform.position = startingPositions[init_position_counter];
				transform.LookAt(obj.transform.position);
				init_position_counter += 1;
	    	}

    		time_counter = 0;

    		if(take_screenshot){
    			ss_name = myObjects[object_counter-1] + (transform.eulerAngles.x.ToString("000")) + "," + (transform.eulerAngles.y.ToString("000")) + "," + (transform.eulerAngles.z.ToString("000"));
    			ScreenshotHandler.TakeScreenshot_Static(Screen.width, Screen.height, ss_name);
    		}
    	}

    }
}
