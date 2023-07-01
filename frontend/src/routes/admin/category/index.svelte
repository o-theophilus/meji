<script context="module">
	import { module } from '$lib/store.js';

	export async function load({ session, fetch }) {
		if (session.user.roles.includes('admin')) {
			const _resp = await fetch(`${import.meta.env.VITE_BACKEND}category`, {
				method: 'get',
				headers: {
					'Content-Type': 'application/json',
					Authorization: session.token
				}
			});

			if (_resp.ok) {
				let resp = await _resp.json();

				if (resp.status == 200) {
					return {
						props: {
							categories: resp.data.categories
						}
					};
				} else {
					return {
						status: 404,
						error: resp.message
					};
				}
			}
		}
		return {
			status: 404,
			error: 'Unauthorised Access'
		};
	}
</script>

<script>
	import { token } from '$lib/cookie.js';
	import { _tick } from '$lib/store.js';

	import Group from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body.svelte';
	import Button from '$lib/comp/button.svelte';
	import SVG from '$lib/comp/svg2.svelte';

	import Edit from './_edit.svelte';

	import Bar from './_bar.svelte';

	$: if ($_tick) {
		categories = $_tick;
		$_tick = '';
		$module = '';
	}

	export let categories;
	let error;

	const move = async (key, dir) => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}category_/${key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ dir })
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				categories = resp.data.categories;
			} else {
				error = resp.message;
			}
		}
	};
</script>

<svelte:head>
	<title>Category | Meji</title>
</svelte:head>

<Group>
	<Title title="Category" />
	<Bar />
	{#if error}
		<p>
			{error}
		</p>
	{/if}
	<Body>
		{#each categories as category}
			<div class="row" draggable="true">
				<Button
					name="{category.name} ({category.count})"
					icon={category.icon}
					class="wide2"
					on:click={() => {
						$module = {
							module: Edit,
							data: category
						};
					}}
				>
					<SVG type={category.icon} size="20" />
				</Button>
				<Button
					name="↑"
					class="cate2"
					on:click={() => {
						move(category.key, 'up');
					}}
				/>
				<Button
					name="↓"
					class="cate2"
					on:click={() => {
						move(category.key, 'down');
					}}
				/>
			</div>
		{:else}
			no category
		{/each}
	</Body>
</Group>

<style>
	.row {
		display: flex;
		align-items: center;
		gap: var(--gap2);
	}
</style>
