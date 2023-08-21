figure();

view (45, 45);

axis([-40,60,-110,10,-180,-120]);

xlabel("X");
ylabel("Y");
zlabel("Z");

for i = 2:21

    plot3(positions(i,1),positions(i,2),positions(i,3), "ro");

    hold on;

    plot3(positions(i,4),positions(i,5) - 50,positions(i,6), "bo");

    plot3(positions(i-1,1),positions(i-1,2),positions(i-1,3), "r.");
    plot3(positions(i-1,4),positions(i-1,5) - 50,positions(i-1,6), "b.");

    hold off;

    fprintf("doing: %d\n",i);

    view (15, 45);

    axis([-40,60,-110,10,-180,-120]);
    
    xlabel("X");
    ylabel("Y");
    zlabel("Z");

    pause(0.25);

end