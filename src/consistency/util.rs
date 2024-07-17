use std::cmp::{Eq, Ord};
use std::fmt::Debug;
use std::hash::Hash;

use std::collections::{HashMap, HashSet};

use std::collections::VecDeque;

use std::collections::BTreeSet;

// Directed Graph
#[derive(Default, Debug, Clone)]
pub struct DiGraph<T>
    where
        T: Hash + Eq + Copy + Debug,
{
    pub adj_map: HashMap<T, HashSet<T>>,
    pub rev_adj_map: HashMap<T, HashSet<T>>,
    pub reachable: HashMap<T, HashSet<T>>,
    pub upd_reachable: bool,
    pub dfs_count: i32,
}


impl<T> DiGraph<T>
    where
        T: Hash + Eq + Copy + Debug,
{
    pub fn init_reachable(&mut self) {
        let us: Vec<T> = self.adj_map.keys().cloned().collect();
        for u in us {
            self.dfs_init_reachable(u);
        }
    }

    pub fn dfs_init_reachable(&mut self, u: T) {
        if !self.reachable.get(&u).is_none() || self.reachable.get(&u).iter().count() > 0 {
            return;
        }

        // u -> v
        if let Some(vs) = self.adj_map.get(&u).cloned() {
            self.dfs_count += 1;
            for &v in vs.iter() {
                self.dfs_init_reachable(v);
                self.reachable.entry(u).or_insert_with(HashSet::new).insert(v);

                let rs = self.reachable.entry(u).or_insert_with(HashSet::new).clone();
                let entry = self.reachable.entry(u).or_insert_with(HashSet::new);
                for &r in rs.iter() {
                    entry.insert(r);
                }
            }
        }
    }

    // upd reachable[u] with reachable[v]
    pub fn dfs_upd_reachable(&mut self, u: T, v: T) {
        let mut change = false;

        let rs = self.reachable.entry(v).or_insert_with(HashSet::new).clone();
        let entry = self.reachable.entry(u).or_insert_with(HashSet::new);

        if entry.insert(v) {
            change = true;
        }

        // r is reachable for v
        for &r in rs.iter() {
            self.dfs_count += 1;
            if entry.insert(r) {
                change = true;
            }
        }

        if !change {
            return;
        }

        // w -> u
        let ws = self.rev_adj_map.entry(u).or_insert_with(HashSet::new).clone();
        for &w in ws.iter() {
            // println!("dfs_upd_reachable above!");
            self.dfs_upd_reachable(w, v);
        }
    }

    pub fn add_edge(&mut self, u: T, v: T) -> bool {
        if self.adj_map.entry(u).or_insert_with(HashSet::new).contains(&v) {
            return false;
        }

        unsafe { EDGE_COUNT += 1; }
        self.adj_map.entry(u).or_insert_with(HashSet::new).insert(v);
        self.rev_adj_map.entry(v).or_insert_with(HashSet::new).insert(u);
        if self.upd_reachable {
            self.dfs_upd_reachable(u, v);
        }
        return true;
    }

    pub fn add_edges(&mut self, u: T, vs: &[T]) {
        // let entry = self.adj_map.entry(u).or_insert_with(HashSet::new);
        for &v in vs {
            // entry.insert(v);
            self.add_edge(u, v);
        }
    }

    pub fn add_vertex(&mut self, u: T) {
        self.adj_map.entry(u).or_insert_with(HashSet::new);
        self.rev_adj_map.entry(u).or_insert_with(HashSet::new);
        self.reachable.entry(u).or_insert_with(HashSet::new);
    }

    pub fn has_edge(&self, u: &T, v: &T) -> bool {
        match self.adj_map.get(u) {
            Some(vs) => vs.contains(v),
            None => false,
        }
    }

    pub fn has_cycle(&self) -> bool {
        self.adj_map.keys().any(|u| {
            // TODO: Memoized search can be faster!
            let mut reachable: HashSet<T> = Default::default();
            self.dfs_util_reach(u, u, &mut reachable)
        })
    }

    // whether s is reachable for u
    fn dfs_util_reach(&self, s: &T, u: &T, reachable: &mut HashSet<T>) -> bool {
        if let Some(vs) = self.adj_map.get(u) {
            for &v in vs.iter() {
                if &v == s || (reachable.insert(v) && self.dfs_util_reach(s, &v, reachable)) {
                    return true;
                }
            }
        }
        false
    }

    // O(n)
    // fn dfs_util_all(&self, u: &T, reachable: &mut HashSet<T>) {
    //     if let Some(vs) = self.adj_map.get(u) {
    //         for &v in vs.iter() {
    //             if reachable.insert(v) {
    //                 // unsafe { dfs_count += 1; }
    //                 self.dfs_util_all(&v, reachable);
    //             }
    //         }
    //     }
    // }

    // connect reachable pairs directly
    // O(n^2)
    pub fn take_closure(&mut self) -> Self {
        DiGraph {
            // adj_map: self
            //     .adj_map
            //     .keys()
            //     .map(|&u| {
            //         let mut reachable: HashSet<T> = Default::default();
            //         self.dfs_util_all(&u, &mut reachable);
            //         // unsafe { dfs_count += 1; }
            //         (u, reachable)
            //     })
            //     .collect(),
            adj_map: self.reachable.clone(),
            rev_adj_map: self.rev_adj_map.clone(),
            reachable: self.reachable.clone(),
            upd_reachable: false,
            dfs_count: 0,
        }
    }

    pub fn union_with(&mut self, g: &Self) -> bool {
        let mut change = false;
        // println!("begin loop");
        for (&u, vs) in g.adj_map.iter() {
            for &v in vs.iter() {
                change |= self.add_edge(u, v);
            }
        }
        change
    }
}

pub(crate) static mut EDGE_COUNT: i32 = 0;

pub trait ConstrainedLinearization {
    type Vertex: Hash + Eq + Copy + Ord + Debug;

    fn get_root(&self) -> Self::Vertex;

    fn children_of(&self, &Self::Vertex) -> Option<Vec<Self::Vertex>>;

    // whether v can be extensions of linearization
    fn allow_next(&self, linearization: &[Self::Vertex], v: &Self::Vertex) -> bool;

    fn vertices(&self) -> Vec<Self::Vertex>;

    fn forward_book_keeping(&mut self, linearization: &[Self::Vertex]);
    fn backtrack_book_keeping(&mut self, linearization: &[Self::Vertex]);

    fn do_dfs(
        &mut self,
        non_det_choices: &mut VecDeque<Self::Vertex>,
        active_parent: &mut HashMap<Self::Vertex, usize>,
        linearization: &mut Vec<Self::Vertex>,
        seen: &mut HashSet<BTreeSet<Self::Vertex>>,
    ) -> bool {
        if !seen.insert(non_det_choices.iter().cloned().collect()) {
            return false;
        }

        if non_det_choices.is_empty() {
            return true;
        }

        let curr_non_det_choices = non_det_choices.len();
        for _ in 0..curr_non_det_choices {
            if let Some(u) = non_det_choices.pop_front() {
                if self.allow_next(linearization, &u) {
                    // access it again
                    if let Some(vs) = self.children_of(&u) {
                        for v in vs {
                            let entry = active_parent
                                .get_mut(&v)
                                .expect("all vertices are expected in active parent");
                            *entry -= 1;
                            if *entry == 0 {
                                non_det_choices.push_back(v);
                            }
                        }
                    }

                    linearization.push(u);

                    self.forward_book_keeping(linearization);

                    if self.do_dfs(non_det_choices, active_parent, linearization, seen) {
                        return true;
                    }

                    self.backtrack_book_keeping(linearization);

                    linearization.pop();

                    if let Some(vs) = self.children_of(&u) {
                        for v in vs {
                            let entry = active_parent
                                .get_mut(&v)
                                .expect("all vertices are expected in active parent");
                            *entry += 1;
                        }
                    }
                    non_det_choices.drain(curr_non_det_choices - 1..);
                }
                non_det_choices.push_back(u);
            }
        }
        return false;
    }

    fn get_linearization(&mut self, status: &mut i32) -> Option<Vec<Self::Vertex>> {
        println!("begin get_linearization");

        // vertice that can be border
        let mut non_det_choices: VecDeque<Self::Vertex> = Default::default();
        // possible parent count
        let mut active_parent: HashMap<Self::Vertex, usize> = Default::default();
        let mut linearization: Vec<Self::Vertex> = Default::default();
        let mut seen: HashSet<BTreeSet<Self::Vertex>> = Default::default();

        // do active_parent counting
        for u in self.vertices() {
            {
                active_parent.entry(u).or_insert(0);
            }
            if let Some(vs) = self.children_of(&u) {
                for v in vs {
                    let entry = active_parent.entry(v).or_insert(0);
                    *entry += 1;
                }
            }
        }

        // take vertices with zero active_parent as non-det choices
        active_parent.iter().for_each(|(v, n)| {
            if *n == 0 {
                non_det_choices.push_back(v.clone());
            }
        });

        println!("begin_dfs");

        self.do_dfs(
            &mut non_det_choices,
            &mut active_parent,
            &mut linearization,
            &mut seen,
        );

        *status = seen.len() as i32;
        println!("cnt of status = {}", status);

        if linearization.is_empty() {
            None
        } else {
            Some(linearization)
        }
    }
}
