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

<section class="line">
	<Button name={$user.setting.item_view} class="tiny" on:click={save_view} />

	|

	<span class="line">
		sort:
		<select bind:value={sort[0]}>
			{#each Object.entries(sorts) as [key, value]}
				<option value={key}>
					{key}
				</option>
			{/each}
		</select>
	</span>

	<!-- <Button name={sort[1] == 'dsc' ? '↑' : '↓'} class="tiny" on:click={direct} /> -->
	<Button
		name={sort[1] == 'dsc' ? sorts[sort[0]][0] : sorts[sort[0]][1]}
		class="tiny"
		on:click={direct}
	/>
	<Button name="Ok" class="tiny" on:click={submit} />
</section>

<style>
	.line {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}
</style>
