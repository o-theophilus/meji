<script>
	import { onMount } from 'svelte';
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Info from '$lib/info.svelte';

	let { item } = $module;
	let tags = item.tags.join(', ');
	let all_tags = [];
	let all_tags_btn = [];
	let error = {};

	onMount(async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tags`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		resp = await resp.json();

		if (resp.status == 200) {
			all_tags = resp.tags;
			clean_value();
		} else {
			error = resp;
		}
	});

	const submit = async () => {
		error = {};

		$loading = true;
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
			$portal = resp.item;

			$module = {
				module: Info,
				status: 200,
				title: '# Details Changed',
				message: 'item tags has been changed successfully',
				button: [
					{
						name: 'Ok',
						icon: 'ok',
						fn: () => {
							$module = '';
						}
					}
				]
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
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Edit Tag</b>
	</svelte:fragment>

	<IG name="tags" {error} let:id>
		<textarea
			bind:value={tags}
			on:blur={() => {
				clean_value();
			}}
			{id}
			placeholder="Tags here"
		/>
	</IG>

	<div class="tags">
		{#each all_tags_btn as tag}
			<Button
				class="tiny"
				name={tag}
				on:click={() => {
					clean_value(tag);
				}}
			/>
		{:else}
			<span class="f2"> loading all tags . . . </span>
		{/each}
	</div>
	<br />
	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}
	<Button class="primary" name="Submit" on:click={submit} />
</Form>

<style>
	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp1);
	}
	.f2 {
		color: var(--ac2);
	}
</style>
