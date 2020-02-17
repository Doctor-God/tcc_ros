
for i  in  $(seq 1 10); do
    import -window "turtlebot3_navigation.rviz* - RViz" -compress None "screenshots/rviz_screen${i}.jpg"
    import -window "Gazebo" -compress None "screenshots/gazebo_screen${i}.jpg"
    sleep 20
done