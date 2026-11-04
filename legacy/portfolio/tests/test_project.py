from pathlib import Path
import sys,unittest
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import project as p

class Tests(unittest.TestCase):
    def test_initial_loss_drawdown(self):
        m=p.risk_metrics(pd.Series([-.1,.0]));self.assertAlmostEqual(m['max_drawdown'],-.1)
    def test_split_no_overlap(self):
        a,b,c=p.split(p.load_data());self.assertLess(a.index.max(),b.index.min());self.assertLess(b.index.max(),c.index.min())
    def test_feasible_minimum_variance(self):
        train,_,_=p.split(p.load_data());w=p.weights(train)
        self.assertTrue(np.allclose(w.sum(),1));self.assertTrue((w>=-1e-10).all().all())
        cov=train.cov().to_numpy();self.assertLessEqual(w.min_variance.to_numpy()@cov@w.min_variance.to_numpy(),w.equal_weight.to_numpy()@cov@w.equal_weight.to_numpy()+1e-9)
    def test_test_data_cannot_change_training_weights(self):
        x=p.load_data();w1=p.weights(p.split(x)[0]);x.loc[x.index>'2021-12-31']+=.1
        pd.testing.assert_frame_equal(w1,p.weights(p.split(x)[0]))
    def test_missing_month_rejected(self):
        x=p.load_data().drop(p.load_data().index[4])
        with self.assertRaises(AssertionError):p.validate(x)
    def test_monthly_rebalance_turnover(self):
        x=pd.DataFrame([[.1,0],[0,0]],columns=['a','b'])
        r,t=p.simulate(x,[.5,.5],100)
        self.assertAlmostEqual(t[0],0);self.assertAlmostEqual(t[1],abs(.55/1.05-.5))
        self.assertLess(r.iloc[1],0)

if __name__=='__main__':unittest.main()
