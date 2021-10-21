# Displays the game using turtle
import turtle

class Display:
	def __init__(self):
		# Turtle setup
		# Screen
		self.wn = turtle.Screen()
		self.wn.title("Snake")
		self.wn.bgcolor("black")
		self.wn.setup(width=800, height=400)
		self.wn.tracer(0)
		# Snake head
		self.head = turtle.Turtle()
		self.head.turtlesize(0.5,0.5)
		self.head.speed(0)
		self.head.shape("square")
		self.head.color("white")
		self.head.penup()
		self.head.goto(205,5)
		self.head.direction = "stop"
		# Snake food
		self.food = turtle.Turtle()
		self.food.turtlesize(0.5,0.5)
		self.food.speed(0)
		self.food.shape("square")
		self.food.color("red")
		self.food.penup()
		# Snake segments
		self.segments = []
		self.buffer_segments = []
		self.add_segments(3)
		# Halfway line
		self.line = turtle.Turtle()
		self.line.speed(0)
		self.line.setposition(0,200)
		self.line.color("white")
		self.line.right(90)
		self.line.forward(400)
		self.line.penup()
		# All the texts
		self.texts = []
		self.text_descriptions = ["Score: ", "High Score: ", "Snakes Alive: ", "Species: #", "Generation: ", "Mode: "]
		self.text_values = [0, 0, 0, 0, 1, "training (1)"]
		for i in range(len(self.text_descriptions)):
			text = turtle.Turtle()
			text.speed(0)
			text.color("white")
			text.penup()
			text.hideturtle()
			# Position text, inserting gaps in certain areas
			if i > 4:
				text.goto(-300, 30+i*-30)
			elif i > 1:
				text.goto(-300, 60+i*-30)
			else:
				text.goto(-300, 90+i*-30)
			text.write(self.text_descriptions[i] + "{}".format(self.text_values[i]), align="left", font=("Avenir Next", 24, "normal"))
			self.texts.append(text)
	# Create additional tail segments
	def add_segments(self,num_segments):
		buffers_used = 0
		for i in range(num_segments):
			if i < len(self.buffer_segments):
				self.buffer_segments[i].goto(205, -5-10*i)
				self.segments.append(self.buffer_segments[i])
				buffers_used += 1
			else:
				new_segment = turtle.Turtle()
				new_segment.turtlesize(0.5,0.5)
				new_segment.speed(0)
				new_segment.shape("square")
				new_segment.color("grey")
				new_segment.penup()
				new_segment.goto(205,-5-10*i)
				self.segments.append(new_segment)
		self.buffer_segments = self.buffer_segments[buffers_used:]
	# Hide extra tail segments
	def hide_segments(self,num_segments):
		for i in range(len(self.segments)-1, len(self.segments)-1-num_segments, -1):
			self.segments[i].goto(1000,1000)
			self.buffer_segments.append(self.segments[i])
		self.segments = self.segments[:len(self.segments)- num_segments]
    # Update screen
	def update(self, head_position, food_position, segment_positions, text_values):
		# Find how many segments are needed
		needed_segments = len(segment_positions) - len(self.segments)
		# Create more segments if needed
		if needed_segments > 0:
			self.add_segments(needed_segments)
		# Hide segments if not needed
		elif needed_segments < 0:
			self.hide_segments(abs(needed_segments))

		# Position head, food, and segments
		self.head.goto(head_position)
		self.food.goto(food_position)
		for i in range(len(segment_positions)):
			self.segments[i].goto(segment_positions[i])
		# Update text
		# For all values
		for i in range(len(text_values)):
			# Check that they are not the same as the currently displayed value
			if self.text_values[i] != text_values[i]:
				# Update currently displayed value
				self.text_values[i] = text_values[i]
				self.texts[i].clear()
				if text_values[i] != -1:
					self.texts[i].write(self.text_descriptions[i]+"{}".format(self.text_values[i]), align="left", font=("Avenir Next", 24, "normal"))