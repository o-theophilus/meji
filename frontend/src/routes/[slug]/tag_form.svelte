<script>
	import { onMount } from 'svelte';
	import { module, portal, loading, toast, state } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Tag from '$lib/button.tag.svelte';
	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Spinner from '$lib/loading_spinner.svelte';

	let item = { ...$module.item };
	let all_tags = [];
	let tags = item.tags.join(', ');
	let all_tags_btn = [];
	let error = {};

	const submit = async () => {
		error = {};

		$loading = 'saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item/${item.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ tags: tags.split(', ').filter(Boolean) })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				type: 'item',
				data: resp.item
			};
			$module = '';
			$toast = {
				status: 200,
				message: 'tag changed'
			};
		} else {
			error = resp;
		}
	};

	const clean_value = (tag = '') => {
		tags = `${tags}, ${tag}`;
		tags = tags.replace(/\r?\n/g, ',');
		tags = tags.replace(/\s+/g, ' ');
		tags = tags.toLowerCase();
		tags = tags.split(',');
		tags = tags.map((i) => i.trim());
		tags = tags.filter(Boolean);
		tags = tags.filter((v, i, l) => l.indexOf(v) === i);
		tags = tags.join(', ');

		all_tags_btn = all_tags.filter((i) => !tags.split(', ').includes(i));
	};

	let loading_tags = true;
	onMount(async () => {
		if (tags == '') {
			tags = item.name.split(' ').join(', ');
		}

		let pn = 'tags';
		let i = $state.findIndex((x) => x.name == pn);
		if (i == -1) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tag`);
			resp = await resp.json();
			loading_tags = false;

			if (resp.status == 200) {
				all_tags = resp.tags;
				$state.push({
					name: pn,
					data: resp.tags
				});
			}
		} else {
			all_tags = $state[i].data;
			loading_tags = false;
		}

		clean_value();
	});
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Edit Tag</b>
	</svelte:fragment>

	<IG
		name="tags"
		{error}
		type="textarea"
		bind:value={tags}
		on:blur={() => {
			clean_value();
		}}
		placeholder="Tags here"
	/>

	<div class="tags_space">
		{#if loading_tags}
			<div class="spinner">
				<Spinner active />
			</div>
		{/if}
		{#each all_tags_btn as tag}
			<Tag
				on:click={() => {
					clean_value(tag);
				}}
			>
				{tag}
			</Tag>
		{/each}
	</div>
	<br />
	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}
	<Button class="primary" on:click={submit}>Save</Button>
</Form>

<style>
	.tags_space {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp1);

		max-height: 200px;
		overflow-y: auto;

		border-radius: var(--sp1);
		padding: var(--sp1);
		border: 2px solid var(--ac4);
	}

	.spinner {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100px;
		width: 100%;
	}
</style>
