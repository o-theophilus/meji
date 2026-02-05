<script>
	import { app } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import Card from './advert.card.svelte';

	let { space, size = null } = $props();
	let loading = true;
	let a300x300 = $state([]);
	let a600x300 = $state([]);
	let a900x300 = $state([]);
	let a300x600 = $state([]);

	onMount(async () => {
		loading = true;

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/adverts?space=${space}`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});

		resp = await resp.json();
		loading = false;

		if (resp.status == 200) {
			for (const x of resp.adverts) {
				if (x.photo['300x300'] && x.space.includes(space)) {
					a300x300.push(x);
				}
				if (x.photo['600x300'] && x.space.includes(space)) {
					a600x300.push(x);
				}
				if (x.photo['900x300'] && x.space.includes(space)) {
					a900x300.push(x);
				}
				if (x.photo['300x600'] && x.space.includes(space)) {
					a300x600.push(x);
				}
			}
		}
	});
</script>

{#if size == '300x300'}
	<div class="card">
		<Card list={a300x300} size="300x300"></Card>
	</div>
{:else if size == '600x300'}
	<div class="card">
		<Card list={a600x300} size="600x300"></Card>
	</div>
{:else if size == '900x300'}
	<div class="card">
		<Card list={a900x300} size="900x300"></Card>
	</div>
{:else}
	<div class="card a300x300">
		<Card list={a300x300} size="300x300"></Card>
	</div>
	<div class="card a600x300">
		<Card list={a600x300} size="600x300"></Card>
	</div>
	<div class="card a900x300">
		<Card list={a900x300} size="900x300"></Card>
	</div>
{/if}

<style>
	.a300x300 {
		display: block;
	}
	.a600x300 {
		display: none;
	}
	.a900x300 {
		display: none;
	}

	@media screen and (min-width: 400px) {
		.a300x300 {
			display: none;
		}
		.a600x300 {
			display: block;
		}
		.a900x300 {
			display: none;
		}
	}
	@media screen and (min-width: 600px) {
		.a300x300 {
			display: none;
		}
		.a600x300 {
			display: none;
		}
		.a900x300 {
			display: block;
		}
	}
</style>
