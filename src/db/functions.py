"""
Available functions for analysis.

All functions defined in `_functions` are created by `client.py`.
"""

from sqlalchemy.sql import func

sql_coalesce = func.coalesce
sql_count = func.count
sql_norm = func.norm
sql_similarity = func.similarity
sql_encode = func.encode

_functions = [
    """
CREATE OR REPLACE FUNCTION norm(arr numeric[])
RETURNS numeric AS $$
DECLARE
    sum_squares numeric := 0;
    i numeric; -- Declaration of the loop variable
BEGIN
    FOREACH i IN ARRAY arr LOOP
        sum_squares := sum_squares + i * i;
    END LOOP;
    RETURN sqrt(sum_squares);
END;
$$ LANGUAGE plpgsql IMMUTABLE;
""",
    """
CREATE OR REPLACE FUNCTION similarity(v1 float[], v2 float[])
RETURNS float AS $$
DECLARE
    dot_product float := 0;
    norm1 float := 0;
    norm2 float := 0;
    i int;
BEGIN
    -- Check if the vectors are not empty and have the same length
    IF v1 IS NULL OR v2 IS NULL OR array_length(v1, 1) != array_length(v2, 1) THEN
        RAISE EXCEPTION 'Vectors must be non-null and of the same length';
    END IF;
    
    -- Calculate dot product and norms of the vectors
    FOR i IN 1..array_length(v1, 1) LOOP
        dot_product := dot_product + v1[i] * v2[i];
        norm1 := norm1 + v1[i] * v1[i];
        norm2 := norm2 + v2[i] * v2[i];
    END LOOP;

    -- Calculate the cosine similarity
    RETURN dot_product / (sqrt(norm1) * sqrt(norm2));
END;
$$ LANGUAGE plpgsql IMMUTABLE STRICT;
""",
]
