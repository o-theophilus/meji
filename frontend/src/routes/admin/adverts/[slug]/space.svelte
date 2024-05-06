<script>
	import { loading, portal, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import Tag from '$lib/button/tag.svelte';

	export let advert;
	export let spaces;
	export let photo_length;
	let selected = [...advert.spaces];

	let error = {};

	const select = (_in) => {
		if (!selected.includes(_in)) {
			selected.push(_in);
			selected = selected;
		} else {
			selected = selected.filter((x) => x != _in);
		}
	};

	const submit = async () => {
		error = {};
		$loading = 'saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/advert/${advert.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ spaces: selected })
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
				message: 'Spaces saved'
			};
		} else {
			error = resp;
		}
	};
</script>

<div>
	<div class="title">Ads Spaces</div>

	<br />

	<div class="spaces">
		{#each spaces as x}
			<Tag
				active={selected.includes(x)}
				on:click={() => {
					select(x);
				}}
				disabled={photo_length(advert) == 0}
			>
				{x}
			</Tag>
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

	<Button
		on:click={submit}
		disabled={photo_length(advert) == 0 ||
			selected.sort().join(', ') == advert.spaces.sort().join(', ')}
	>
		Save Space
	</Button>
</div>

<style>
	.title {
		font-weight: 900;
	}

	.spaces {
		display: flex;
		gap: var(--sp1);
		flex-wrap: wrap;
	}
</style>
