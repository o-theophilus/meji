<script context="module">
	import { module } from '$lib/store.js';

	export async function load({ session, fetch }) {
		if (session.user.roles.includes('admin')) {
			const _resp = await fetch(`${import.meta.env.VITE_BACKEND}tag`, {
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
							tags: resp.data.tags
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

	import Group from '$lib/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/comp/svg2.svelte';

	import Edit from './_edit.svelte';

	import Bar from './_bar.svelte';

	$: if ($_tick) {
		tags = $_tick;
		$_tick = '';
		$module = '';
	}

	export let tags;
	let error;

	const move = async (key, dir) => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}tag_/${key}`, {
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
				tags = resp.data.tags;
			} else {
				error = resp.message;
			}
		}
	};
</script>

<svelte:head>
	<title>tag | Meji</title>
</svelte:head>

<Group>
	<Title title="tag" />
	<Bar />
	{#if error}
		<p>
			{error}
		</p>
	{/if}
	<Body>
		{#each tags as tag}
			<div class="row" draggable="true">
				<Button
					name="{tag.name} ({tag.count})"
					icon={tag.icon}
					class="wide2"
					on:click={() => {
						$module = {
							module: Edit,
							data: tag
						};
					}}
				>
					<SVG type={tag.icon} size="20" />
				</Button>
				<Button
					name="↑"
					class="cate2"
					on:click={() => {
						move(tag.key, 'up');
					}}
				/>
				<Button
					name="↓"
					class="cate2"
					on:click={() => {
						move(tag.key, 'down');
					}}
				/>
			</div>
		{:else}
			no tag
		{/each}
	</Body>
</Group>

<style>
	.row {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}
</style>
