# Motor Vehicle Collision in NYC Analysis
## General
Given the increasing reports of road accidents, this application
was made in order to have a better insight regarding motor vehicle accidents
specifically. We have collected data from various sources and store them in
a csv file, that can be found [here]. This file is used to create a dashboard with
interactive plots, 3D maps, etc. With the use of sliders, select-boxes and dropdowns,
each users can define their choices and watch the diagrams to change dynamically. First, 
they can see in a map where the most accidents happened, based on the number of injured people.
They can also specify a desired hour, and observe in a 3D map how many accidents and
where those accidents happened at the time given (with 1 hour interval). Finally, 
the app also display the most dangerous streets for pedestrians, cyclists or motorists

## Libraries Used
The app was based on [Streamlit]. Apart from it, the following libraries were used:
* pandas
* numpy
* pydeck
* plotly


## Execution
To start the web app, open a terminal in the home directory of the project (/"DataScience Web App").
Then, just type the below command:
```shell
streamlit run app.py
```

## Final Notes
Due to the csv file being approximatelly 180 MB, it is contained in a zip format inside "resources" folder. For the python script
to run successfully please extract the file to the same folder.



[here]: /resources/Motor_Vehicle_Collisions.csv
[Streamlit]: https://streamlit.io/
