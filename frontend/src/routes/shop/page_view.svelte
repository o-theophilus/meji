<script>
	import { set_state } from '$lib/store.js';
	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import Button from '$lib/button.svelte';

	export let page_name = '';
	let sort = ['date', 'dsc'];

	let sorts = {
		date: ['old-new', 'new-old'],
		name: ['z-a', 'a-z'],
		price: ['hi-lo', 'lo-hi'],
		discount: ['hi-lo', 'lo-hi']
		// 'rating'
	};
	let sorts2 = [
		'latest',
		'oldest',
		'name (a-z)',
		'name (z-a)',
		'cheap',
		'expensive',
		'discount'
		// 'rating'
	];

	const save_view = async () => {
		$user.setting.item_view = $user.setting.item_view == 'grid' ? 'list' : 'grid';
		const resp = await fetch(`${import.meta.env.VITE_BACKEND}/setting`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ item_view: $user.setting.item_view })
		});
	};
	const direct = () => {
		sort[1] = sort[1] == 'dsc' ? 'asc' : 'dsc';
	};
	const submit = () => {
		let a = sort.join(',');
		if (a == 'date,dsc') {
			a = '';
		}
		set_state(page_name, 'sort', a);
	};
</script>

<section class="line wrap">
	<Button class="small" on:click={save_view}>
		{$user.setting.item_view}
	</Button>

	|

	<span class="line">
		sort:
		<select bind:value={sort[0]}>
			{#each Object.keys(sorts) as key}
				<option value={key}>
					{key}
				</option>
			{/each}
		</select>
	</span>

	<Button class="small" on:click={direct}>
		{sort[1] == 'dsc' ? sorts[sort[0]][0] : sorts[sort[0]][1]}
	</Button>
	<Button class="small" on:click={submit}>Ok</Button>
</section>

<style>
	.line {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}
	.wrap {
		flex-wrap: wrap;
	}

	select {
		display: inline;
	}
</style>
