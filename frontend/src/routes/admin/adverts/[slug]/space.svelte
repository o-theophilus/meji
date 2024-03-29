<script>
	import { loading, portal, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Check from '$lib/button.check.svelte';

	export let advert;
	export let spaces;
	export let disabled;
	let error = {};

	$: s_spaces = advert.spaces;

	const select = (_in) => {
		if (!s_spaces.includes(_in)) {
			s_spaces.push(_in);
			s_spaces = s_spaces;
		} else {
			s_spaces = s_spaces.filter((x) => x != _in);
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
			body: JSON.stringify({ spaces: s_spaces })
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
			<Check
				active={s_spaces.includes(x)}
				on:click={() => {
					select(x);
				}}
				{disabled}
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

	<Button class="primary" on:click={submit} {disabled}>Save Space</Button>
</div>

<style>
	.title {
		font-weight: 600;
	}

	.spaces {
		display: flex;
		gap: var(--sp1);
		flex-wrap: wrap;
	}
</style>
