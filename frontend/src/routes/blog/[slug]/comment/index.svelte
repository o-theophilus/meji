<script>
	import { app, module, scroll } from '$lib/store.svelte.js';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { slide } from 'svelte/transition';

	import { Login } from '$lib/auth';
	import { Button, FoldButton, RoundButton } from '$lib/button';
	import { PageNote } from '$lib/info';
	import { Dropdown, Pagination } from '$lib/input';
	import { Icon, Spinner } from '$lib/macro';
	import Add from './_add.svelte';
	import Control from './one.control.svelte';
	import One from './one.svelte';

	let { blog, comment_resp, loading } = $props();

	let comments = $derived(comment_resp.comments);
	let total_comment = $derived(comment_resp.total_comment);
	let total_page = $derived(comment_resp.total_page);
	let order_by = $derived(comment_resp.order_by);
	let searchParams = $derived(comment_resp.searchParams);
	let pagination = $state();

	let open = $derived(comments?.length > 0);

	const update = (a, b, c) => {
		comments = a;
		total_comment = b;
		total_page = c;
	};

	export const load = async () => {
		loading = true;

		let response = await fetch(
			`${import.meta.env.VITE_BACKEND}/blogs/${blog.key}/comments?${new URLSearchParams(searchParams).toString()}`,
			{
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				}
			}
		);
		let result = await response.json();

		if (response.status == 200) {
			comments = result.comments;
		}

		loading = false;
		scroll('#comment_section');
	};
</script>

<div class="line space comment_section">
	<div class="line">
		<span class="page_title">
			{#if total_comment > 0}
				{total_comment}
			{/if}
			Comment{#if total_comment > 1}s{/if}
		</span>
		<Spinner active={loading} size="20" />
	</div>

	{#if !loading}
		<FoldButton
			{open}
			onclick={() => {
				open = !open;
			}}
		/>
	{/if}
</div>

{#if open && !loading}
	<div
		class="comment_area"
		transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}
	>
		{#if comments?.length > 1}
			<div class="line space">
				<div></div>
				<Dropdown
					--select-height="1"
					--select-padding-x="0"
					--select-font-size="0.8rem"
					--select-background-color="transparent"
					--select-background-color-hover="transparent"
					--select-color="var(--ft2)"
					--select-color-hover="var(--ft1)"
					--select-outline-color="transparent"
					label="Sort: {searchParams.order}"
					list={order_by}
					icon="arrow-down-up"
					icon2="chevron-down"
					bind:value={searchParams.order}
					onchange={(v) => {
						searchParams.page_no = 1;
						pagination.reset();
						load();
					}}
				/>
			</div>
		{/if}

		{#each comments as comment (comment.key)}
			<div class="comment" animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
				<div class="main">
					<One {comment}></One>
					<Control {comment} {blog} {searchParams} {update}>
						{#snippet reply()}
							<RoundButton
								icon="reply"
								onclick={() => module.open(Add, { comment, blog, searchParams, update })}
							/>
						{/snippet}
					</Control>
				</div>
				{#each comment.replies as reply (reply.key)}
					<div class="reply" animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
						<One comment={reply}></One>
						<Control comment={reply} {blog} {searchParams} {update}></Control>
					</div>
				{/each}
			</div>
		{:else}
			<PageNote>
				<Icon icon="message-circle-off" size="50" />
				No comment
			</PageNote>
		{/each}

		<Pagination
			{total_page}
			bind:this={pagination}
			bind:value={searchParams.page_no}
			ondone={(v) => {
				load();
			}}
		></Pagination>
	</div>
{/if}

<div class="button">
	{#if app.login}
		<Button
			icon="message-circle-plus"
			onclick={() => module.open(Add, { blog, update, searchParams })}
		>
			Add comment
		</Button>
	{:else}
		<Button icon="log-in" onclick={() => module.open(Login)}>Login to add comment</Button>
	{/if}
</div>

<style>
	.comment_section {
		margin-top: 24px;
		border-top: 1px solid var(--ft1);
		padding-top: 24px;
	}

	.comment_area {
		margin-top: 16px;
	}

	.comment {
		margin-top: 8px;

		border-radius: 8px;
		overflow: hidden;
		outline: 1px solid var(--ol);
		outline-offset: -1px;
	}

	.main {
		padding: 16px;
		background-color: var(--bg3);
	}
	.reply {
		border-top: 1px solid var(--ol);
		padding: 16px;
		background-color: var(--bg2);
	}

	.button {
		margin-top: 16px;
	}
</style>
