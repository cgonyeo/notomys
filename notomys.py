import Leap, sys, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from predestinate import MouseGod


class MouseListener(Leap.Listener):

	def on_init(self, controller):
		self.mg = MouseGod()
		self.lastX = -1
		self.lastY = -1
		self.sensitivity = 5
		self.thumbVanishTime = 0
		self.lastFingerCount = 0
		self.lastClickTime = 0
		self.fingerId = 0
		self.thumbId = 0
		self.seenIds = []
		print "Initialized"

	def on_connect(self, controller):
		print "Connected"
	
	def on_disconnect(self, controller):
		# Note: not dispatched when running in a debugger.
		print "Disconnected"
	
	def on_exit(self, controller):
		print "Exited"
	
	def on_frame(self, controller):
		# Get the most recent frame and report some basic information
		frame = controller.frame()

		if not frame.hands.empty:
			# Get the first hand
			hand = frame.hands[0]
			self.seenIds = []
		
			# Check if the hand has any fingers
			fingers = hand.fingers
			if frame.finger(self.fingerId).id == -1 and len(fingers) > 0:
				self.fingerId = fingers[0].id
			if frame.finger(self.thumbId).id == -1 and len(fingers) > 1 and fingers[len(fingers) - 1].id not in self.seenIds:
				self.thumbId = fingers[len(fingers) - 1].id

			if not fingers.empty:
				if self.lastFingerCount == len(fingers) + 1 and self.lastFingerCount > 1:
					print "thumb lost"
					self.thumbVanishTime = time.time()
				elif self.lastFingerCount == len(fingers) - 1 and self.lastFingerCount > 0:
					print "thumb gained"
					if time.time() - self.thumbVanishTime < 1 and time.time() - self.lastClickTime > 0.25:
						print "click"
						self.mg.click(1)
						self.lastClickTime = time.time()

				finger = frame.finger(self.fingerId)
				currentX = finger.tip_position.x
				currentY = finger.tip_position.y * -1
				currentZ = finger.tip_position.z

				if(self.lastX != -1 and currentZ < 0):
					deltaX = currentX - self.lastX
					deltaY = currentY - self.lastY
					self.mg.move(int(deltaX * self.sensitivity), int(deltaY * self.sensitivity), True)

				self.lastX = currentX
				self.lastY = currentY
			else:
				self.lastX = -1
				self.lastY = -1
			self.lastFingerCount = len(fingers)

			for f in fingers:
				self.seenIds.append(f.id)

		
	def state_string(self, state):
		if state == Leap.Gesture.STATE_START:
			return "STATE_START"
		
		if state == Leap.Gesture.STATE_UPDATE:
			return "STATE_UPDATE"
		
		if state == Leap.Gesture.STATE_STOP:
			return "STATE_STOP"
		
		if state == Leap.Gesture.STATE_INVALID:
			return "STATE_INVALID"

def main():
	# Create a sample listener and controller
	listener = MouseListener()
	controller = Leap.Controller()
	
	# Have the sample listener receive events from the controller
	controller.add_listener(listener)
	
	# Keep this process running until Enter is pressed
	print "Press Enter to quit..."
	sys.stdin.readline()
	
	# Remove the sample listener when done
	controller.remove_listener(listener)


if __name__ == "__main__":
	main()
