


class ModelQueue:

	def __init__(self, num_bins=64):
		self.bins = [ [] for i in range(num_bins)]
		self.dirty = [ False for i in range(num_bins)]


	def push(self,model):
		self.bins[model.size()].append(model)
		self.dirty[model.size()] = True
		pass


	def pop(self, cnt):
		# self._sort()
		pops = []
		while len(pops) < cnt:
			last = None

			for i,bin in enumerate( self.bins ):
			# for i,bin in enumerate( reversed(self.bins) ):
			# 	i = 63-i

				# early break
				if len(pops) == cnt:
					return pops

				if len(bin) == 0:
					continue

				if self.dirty[i]:
					bin.sort(key=lambda m: m.score, reverse=True)
					self.dirty[i] = False

				curr = bin[-1]


				if last == None:
					last = curr
					continue
				
				diff = curr.score - last.score
				diff_sz = curr.size() - last.size()

				# print i, diff
				# print "  ", last
				# print "  ", curr

				if diff_sz < 0:
					print "ERROR: size diff should always positive"
					return

				# XXX seems to be an error here
				# should see both 0.002... expressions
				# when solving F_1 test

				# if diff < 0:
					# last = curr
					# continue

				if diff < 0:
					popd = self.bins[last.size()].pop()
					self.dirty[last.size()] = True
					pops.append(popd)

					# print " ++++ ", popd

					if len(pops) + 1 == cnt:
						popd = self.bins[curr.size()].pop()
						self.dirty[curr.size()] = True
						pops.append(popd)
						return pops

					last = curr

			if last is not None:
				popd = self.bins[last.size()].pop()
				self.dirty[last.size()] = True
				pops.append(popd)

	def sort(self):
		for i,bin in enumerate(self.bins):
			self.bins[i].sort(key=lambda m: m.score, reverse=True)
			self.dirty[i] = False


	def _sort(self):
		for i,dty in self.dirty:
			if dty:
				self.bins[i].sort(key=lambda m: m.score, reverse=True)
				self.dirty[i] = False



	def do_print(self):
		offset = 3
		for i,bin in enumerate(self.bins[offset:15]):
			print i+offset, len(bin), self.dirty[i]
			for j,m in enumerate(bin):
				print "   ", j, m.score, m.expr
			print ""













