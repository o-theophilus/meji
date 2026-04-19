<script>
	import { afterNavigate, replaceState } from '$app/navigation';
	import { page } from '$app/state';
	import { app } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';

	import { Switch } from '$lib/button';
	import { Content } from '$lib/layout';
	import { Log, Meta } from '$lib/macro';

	import { Author, Comment, Content_, Date, Description, Photo, Status, Tags, Title } from '.';
	import Engagement from './engage/engagement.svelte';
	import Like from './engage/like.svelte';
	import Share from './engage/share.svelte';
	import Similar from './similar.svelte';
	import ToTop from './to_top.svelte';

	let { data } = $props();
	let blog = $derived(data.blog);
	let edit_mode = $state(false);
	let is_admin = app.user.access.some((x) =>
		[
			'blog.add',
			'blog.edit_photo',
			'blog.edit_title',
			'blog.edit_date',
			'blog.edit_description',
			'blog.edit_content',
			'blog.edit_files',
			'blog.edit_tags',
			'blog.edit_status',
			'blog.edit_author',
			'blog.edit_featured'
		].includes(x)
	);

	let loading = $state(false);
	let engagement = $state({});
	let author = $state({});
	let comment_resp = $state([]);
	let similar = $state([]);

	const update = async (data) => {
		blog = data;
	};

	const hard_update = async (data) => {
		blog = data;
		edit_mode = false;
		loading = true;

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/blogs/${blog.key}/after`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});

		resp = await resp.json();
		loading = false;

		if (resp.status == 200) {
			engagement = resp.engagement;
			author = resp.author;
			comment_resp = resp.comment_resp;
			similar = resp.similar;
		}
	};

	onMount(async () => {
		if (page.url.searchParams.has('edit') && is_admin) {
			page.url.searchParams.delete('edit');
			edit_mode = true;
			replaceState(page.url.href);
		}
	});

	afterNavigate(() => hard_update(blog));
</script>

{#key blog.key}
	<Log action={'viewed'} entity_key={blog.key} entity_type={'blog'} />
{/key}
<Meta title={blog.title} description={blog.description} image={blog.photo} />

<Content --content-background-color="var(--bg)">
	{#if is_admin}
		<Switch
			--toggle-height="21px"
			--toggle-font-size="0.8rem"
			--toggle-padding-x="8px"
			list={['', 'edit']}
			value={!edit_mode ? '' : 'edit'}
			onclick={() => {
				edit_mode = !edit_mode;
			}}
		/>

		<br />
	{/if}

	<Status {blog} {edit_mode} {update}></Status>
	<Photo bind:blog {edit_mode} {update} />
	<Title {blog} {edit_mode} {update} />
	<Description {blog} {edit_mode} {update} />
	<div class="line space date">
		<Date {blog} {edit_mode} {update}></Date>
		<Engagement {engagement} {loading}></Engagement>
	</div>
	<Content_ {blog} {edit_mode} {update}></Content_>
	<Tags {blog} {edit_mode} {update}></Tags>
	<Author {author} {blog} {edit_mode} {loading} update={hard_update} />
</Content>

<Content --content-height>
	<div class="line engage">
		<Like {blog} bind:engagement />
		<Share {blog} />
	</div>

	<Comment {blog} {comment_resp} {loading} />
	<ToTop />
</Content>

<Similar {similar} {loading} />

<style>
	.line.date {
		align-items: flex-end;
	}
	.line.engage {
		gap: 16px;
	}
</style>
