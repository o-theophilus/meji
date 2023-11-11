<script>
	import { loading, portal, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Check from '$lib/button.check.svelte';

	export let advert;
	export let ad_space;
	let error = {};

	let places = advert.places;

	const select = (_in) => {
		if (!places.includes(_in)) {
			places.push(_in);
			places = places;
		} else {
			places = places.filter((x) => x != _in);
		}
	};

	let available_sizes = [];
	$: {
		available_sizes = [];
		for (const [dim, url] of Object.entries(advert.photos)) {
			if (url) {
				available_sizes.push(dim);
			}
		}
		available_sizes = available_sizes;
	}

	const submit = async () => {
		error = {};
		$loading = 'saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/advert_placement/${advert.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ places })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				type: 'advert',
				data: resp.advert
			};
			$toast = {
				status: 200,
				message: 'Placement saved'
			};
		} else {
			error = resp;
		}
	};
</script>

<div>
	<div class="title">Placement</div>

	<br />

	<div class="placements">
		{#each ad_space as x}
			<Check
				active={places.includes(x)}
				on:click={() => {
					select(x);
				}}
			>
				{x}
			</Check>
		{/each}
	</div>

	<br />
	{#if error.error}
		<span class="error">
			{error.error}
		</span>
		<br />
		<br />
	{/if}

	<Button class="primary" on:click={submit} disabled={available_sizes.length != 4}>
		Save Placement
	</Button>
	<br />
	<Button class="link" href="/{advert.item.slug}">{advert.item.name} &gt;</Button>
</div>

<style>
	.title {
		font-weight: 600;
	}

	.placements {
		display: flex;
		gap: var(--sp1);
		flex-wrap: wrap;
	}
</style>
