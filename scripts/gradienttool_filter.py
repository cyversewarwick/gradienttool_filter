import math
import argparse

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--Input', dest='input', type=argparse.FileType('r'), required=True, help='CSV output generated by the gradient tool.')
	parser.add_argument('--Threshold', dest='thresh', type=float, default=2, help='Threshold to apply to the gradient tool z-scores to quantify the times at which regulatory events take place. Default: 2')
	args = parser.parse_args()
	args.thresh = abs(args.thresh)
	return args

def main():
	args = parse_args()
	lines = args.input.readlines()
	#lose header
	del lines[0]
	#prepare output file
	out = [['Gene ID','First Up','First Down','First Change']]
	for line in lines:
		line = line.strip().split(',')
		#down-regulation?
		if float(line[-1])<=(-1*args.thresh):
			if line[0]!=out[-1][0]:
				#finalise prior record
				for j in range(1,4):
					out[-1][j] = str(out[-1][j])
				#add new record
				out.append([line[0],float('nan'),float(line[1]),float(line[1])])
			else:
				#no need to check if it's better than the prior stored value, as if it's stored it's earlier
				#as such, it might be first down after there already is a first up
				if math.isnan(out[-1][2]):
					out[-1][2] = float(line[1])
		#repeat for up-regulation
		if float(line[-1])>=args.thresh:
			if line[0]!=out[-1][0]:
				#finalise prior record
				for j in range(1,4):
					out[-1][j] = str(out[-1][j])
				#add new record
				out.append([line[0],float(line[1]),float('nan'),float(line[1])])
			else:
				#no need to check if it's better than the prior stored value, as if it's stored it's earlier
				#as such, it might be first up after there already is a first down
				if math.isnan(out[-1][1]):
					out[-1][1] = float(line[1])
	#process final record
	for j in range(1,4):
		out[-1][j] = str(out[-1][j])
	#export
	toggle = ''
	with open('ChangingGenes.txt','w') as fid:
		for line in out:
			fid.write(toggle+'\t'.join(line))
			toggle = '\n'

if __name__ == "__main__":
	main()