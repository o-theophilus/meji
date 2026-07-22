<script>
	import { Button, RoundButton, Tag } from '$lib/button';
	import { Note } from '$lib/info';
	import { IG, Input } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	let error = $state({});
	let filter = $state('');
	let form = $state({});
	let all = $derived.by(() => {
		let _temp = app.item_all_tags;
		if (filter) {
			_temp = _temp.filter((x) => x.toLowerCase().includes(filter.toLowerCase()));
		}
		return _temp;
	});

	const validate = () => {
		error = {};

		if (!form.old) {
			error.old = 'Choose the tag to rename';
		}
		if (!form.tag) {
			error.tag = 'This field is required';
		} else if (form.old && form.old === form.tag) {
			error.tags = 'No changes were made';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		loading.open('Renaming Tag . . .');
		let result = await fetch(`${import.meta.env.VITE_BACKEND}/items/tag/rename`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		result = await result.json();
		loading.close();

		if (result.status == 200) {
			app.item_all_tags = result.all;
			app.item_featured_tags = result.featured;
			module.close();
			notify.open('Tag Renamed');
		} else {
			error = result;
		}
	};
</script>

<Form title="Renme Tag" error={error.error}>
	{#if form.old}
		<Tag>
			{form.old}
		</Tag>
	{:else}
		<Note status={error.old ? 400 : null} note="Choose the tag to rename"></Note>
	{/if}

	<IG
		name="Name"
		icon="square-pen"
		error={error.tag}
		placeholder="New tag name here"
		type="text"
		bind:value={form.tag}
	/>

	<IG name="All">
		{#snippet input()}
			<div class="block">
				<div class="search">
					<Input placeholder="filter" bind:value={filter}>
						{#snippet right()}
							{#if filter}
								<div class="clear">
									<RoundButton
										--button-background-color-hover="red"
										icon="x"
										onclick={() => (filter = '')}
									></RoundButton>
								</div>
							{/if}
						{/snippet}
					</Input>
				</div>

				<div class="tags">
					{#each all as x (x)}
						<div class="tag" animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
							<Tag
								onclick={() => {
									form.old = x;
									form.tag = x;
									error = {};
								}}
							>
								{x}
							</Tag>
						</div>
					{/each}
				</div>
			</div>
		{/snippet}
	</IG>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>

<style>
	.block {
		outline: 1px solid var(--ol);
		outline-offset: -1px;
		border-radius: 4px;
		padding: 8px;
	}

	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 4px;

		max-height: 200px;
		overflow: auto;
	}

	.search {
		margin-bottom: 8px;
		.clear {
			margin-right: 8px;
		}
	}
</style>
