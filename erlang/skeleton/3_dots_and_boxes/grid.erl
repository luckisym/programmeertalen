-module(grid).
-export([show_hlines/2, show_vlines/2, print/1, new/2, get_wall/3, has_wall/2, add_wall/2, get_cell_walls/2, get_all_walls/2, get_open_spots/1, choose_random_wall/1]).

% TODO: The other functions.
new(Width, Height) -> 
    {Width, Height, []}.

get_wall(X, Y, Dir) -> 
    case Dir of
        north -> {{X, Y - 1}, {X, Y}};
        east -> {{X, Y}, {X + 1, Y}};
        south -> {{X, Y}, {X, Y + 1}};
        west -> {{X -1, Y}, {X, Y}}
    end.

has_wall(Wall, Grid) ->
    {_, _, Walls} = Grid,
    lists:member(Wall, Walls).

add_wall(Wall, Grid) ->
    {Width, Height, Walls} = Grid,
    case has_wall(Wall, Grid) of
        true->
            Grid;
        false ->
            UpdatedWalls = [Wall|Walls], 
            {Width, Height, UpdatedWalls}
    end.

place_wall(X, Y, Dir, Grid, Wall, Empty) ->
    case has_wall(get_wall(X, Y, Dir), Grid) of 
        true -> Wall;
        false -> Empty
    end.

show_hlines(Row, Grid) -> 
    {Width, _, _} = Grid, 
    Hlines = lists:map(fun(X) -> 
        place_wall(X, Row, south, Grid, "+--", "+  "),
        place_wall(X, Row, north, Grid, "+--", "+  ")
    end, lists:seq(0, Width-1)), 
    lists:concat(Hlines) ++ "+~n".

% TODO
show_vlines(Row, Grid) -> 
    {Width, _, _} = Grid, 
    Vlines = lists:map(fun(X) -> 
        place_wall(X, Row, east, Grid, "|  ", "   "),
        place_wall(X, Row, west, Grid, "|  ", "   ")
    end, lists:seq(0, Width - 1)),
    lists:concat(Vlines) ++ place_wall(Width - 1, Row, east, Grid, "|~n", " ~n").

get_cell_walls(X, Y) ->
    [
        get_wall(X, Y, north),
        get_wall(X, Y, east),
        get_wall(X, Y, west),
        get_wall(X, Y, south)
    ].

get_all_walls(W, H) ->
    Walls = [get_cell_walls(X, Y) || X <- lists:seq(0, W - 1), Y <- lists:seq(0, H - 1)], 
    lists:usort(lists:flatten(Walls)).

get_open_spots(Grid) ->
    {W, H, Walls} = Grid, 
    lists:subtract(get_all_walls(W, H), Walls).

choose_random_wall(Grid) ->
    Options = get_open_spots(Grid),
    case Options of
        [] -> 
            [];
        _ ->
            RandomIndex = rand:uniform(length(Options)),
            lists:nth(RandomIndex, Options)
    end.


% Prints this grid in a structured format
% using the show_Xlines functions.
print(Grid) ->
    {_, H, _} = Grid,
    lists:map(fun(Row) ->
        io:fwrite(show_hlines(Row, Grid)),

        case Row < H of
            true ->
                io:fwrite(show_vlines(Row, Grid));
            false ->
                ok
        end
    end, lists:seq(0, H)),
    io:fwrite("~n"),
    ok.
