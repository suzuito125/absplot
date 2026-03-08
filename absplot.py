# Copyright (c) 2025, Suzu Ito <https://github.com/suzuito125>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause License.
# See the LICENSE file in the project root for details.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker

# Default settings
TICKS_FONTSIZE = 10
TICKS_DIRECTION = 'in'
TICKS_COLOR = 'black'
TICKS_LENGTH = 3.5
TICKS_WIDTH = 0.75
TICKS_LABEL_XPAD = 5
TICKS_LABEL_YPAD = 3

class MainFrame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fig = plt.figure(figsize=(self.width / 25.4, self.height / 25.4))
        self.fig_div_list = np.array([self.width, self.height, self.width, self.height])
        self.ax = self.fig.add_axes(np.array([0, 0, self.width, self.height]) / self.fig_div_list)
        # [left, bottom, width, height] (mm units)
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        self.ax.axes.xaxis.set_visible(False)
        self.ax.axes.yaxis.set_visible(False)
        self.ax.set_axis_off()


class EmptyFrame:
    def __init__(self, mainframe, left, bottom, width, height):
        ax_dim_list_ = [left, bottom, width, height]  # mm units
        self.ax = mainframe.fig.add_axes(np.array(ax_dim_list_) / mainframe.fig_div_list)
        self.ax.set_facecolor('none')
        self.ax.axes.xaxis.set_visible(False)
        self.ax.axes.yaxis.set_visible(False)
        self.ax.set_axis_off()
        axframes_pos_array_ = np.array(self.ax.get_position())
        self.left = axframes_pos_array_[0, 0] * mainframe.width  # mm unit
        self.bottom = axframes_pos_array_[0, 1] * mainframe.height  # mm unit
        self.width = (axframes_pos_array_[1, 0] - axframes_pos_array_[0, 0]) * mainframe.width  # mm unit
        self.height = (axframes_pos_array_[1, 1] - axframes_pos_array_[0, 1]) * mainframe.height  # mm unit
        self.ax.set_xlim(self.left, self.left + self.width)
        self.ax.set_ylim(self.bottom, self.bottom + self.height)

    def visualize_frame(self):
        self.ax.set_axis_on()


class PlotFrame:
    def __init__(self, mainframe, parentframe, left, bottom, width, height,
                 ticks_fontsize=TICKS_FONTSIZE, ticks_direction=TICKS_DIRECTION,
                 ticks_length=TICKS_LENGTH, ticks_width=TICKS_WIDTH, ticks_color=TICKS_COLOR,
                 ticks_label_xpad=TICKS_LABEL_XPAD, ticks_label_ypad=TICKS_LABEL_YPAD):
        self.mainframe = mainframe
        self.parentframe = parentframe
        self.left = left
        self.bottom = bottom
        self.width = width
        self.height = height

        # [left, bottom, width, height] (mm units)
        self.ax_dim_list = [parentframe.left + self.left, parentframe.bottom + self.bottom, self.width, self.height]
        self.ax = mainframe.fig.add_axes(np.array(self.ax_dim_list) / mainframe.fig_div_list)

        # default appearance
        self.ax.tick_params(axis='x', labelsize=ticks_fontsize, direction=ticks_direction,
                            length=ticks_length, width=ticks_width, color=ticks_color,
                            top=True, pad=ticks_label_xpad)
        self.ax.tick_params(axis='y', labelsize=ticks_fontsize, direction=ticks_direction,
                            length=ticks_length, width=ticks_width, color=ticks_color,
                            right=True, pad=ticks_label_ypad)

        # no top and right axes by default
        self.ax_top = None
        self.ax_right = None
        # no imshow by default
        self.imshow = None
        # no colorbar by default
        self.cax = None
        self.cax_dim_list = None

    def hide_axis(self):
        self.ax.axes.xaxis.set_visible(False)
        self.ax.axes.yaxis.set_visible(False)

    def hide_frame(self):
        self.ax.set_axis_off()

    def add_right_axis(self, ticks_fontsize=TICKS_FONTSIZE, ticks_direction=TICKS_DIRECTION,
                       ticks_length=TICKS_LENGTH, ticks_width=TICKS_WIDTH, ticks_color=TICKS_COLOR,
                       ticks_label_ypad=TICKS_LABEL_YPAD):
        self.ax_right = self.ax.twinx()
        self.ax.tick_params(axis='y', right=False)
        self.ax_right.tick_params(axis='y', labelsize=ticks_fontsize, direction=ticks_direction,
                                  length=ticks_length, width=ticks_width, color=ticks_color, 
                                  pad=ticks_label_ypad)

    def add_top_axis(self, ticks_fontsize=TICKS_FONTSIZE, ticks_direction=TICKS_DIRECTION,
                     ticks_length=TICKS_LENGTH, ticks_width=TICKS_WIDTH, ticks_color=TICKS_COLOR,
                     ticks_label_xpad=TICKS_LABEL_XPAD):
        self.ax_top = self.ax.twiny()
        self.ax.tick_params(axis='x', top=False)
        self.ax_top.tick_params(axis='x', labelsize=ticks_fontsize, direction=ticks_direction,
                                length=ticks_length, width=ticks_width, color=ticks_color, 
                                pad=ticks_label_xpad)

    def modify_ticks(self, ticks_fontsize=TICKS_FONTSIZE,
                     ticks_direction=TICKS_DIRECTION, reflect_top=True, reflect_right=True,
                     ticks_length=TICKS_LENGTH, ticks_width=TICKS_WIDTH, ticks_color=TICKS_COLOR,
                     ticks_label_xpad=TICKS_LABEL_XPAD, ticks_label_ypad=TICKS_LABEL_YPAD):
        self.ax.tick_params(axis='x', labelsize=ticks_fontsize, direction=ticks_direction,
                            length=ticks_length, width=ticks_width, color=ticks_color,
                            top=reflect_top, pad=ticks_label_xpad)
        self.ax.tick_params(axis='y', labelsize=ticks_fontsize, direction=ticks_direction,
                            length=ticks_length, width=ticks_width, color=ticks_color,
                            right=reflect_right, pad=ticks_label_ypad)
        if self.ax_right is not None:
            self.ax.tick_params(axis='y', right=False)
            self.ax_right.tick_params(axis='y', labelsize=ticks_fontsize, direction=ticks_direction,
                                      length=ticks_length, width=ticks_width, color=ticks_color, pad=ticks_label_ypad)
        if self.ax_top is not None:
            self.ax.tick_params(axis='x', top=False)
            self.ax_top.tick_params(axis='x', labelsize=ticks_fontsize, direction=ticks_direction,
                                    length=ticks_length, width=ticks_width, color=ticks_color, pad=ticks_label_xpad)

    def add_colorbar(self, cleft, cbottom, cwidth, cheight,
                     ticks_fontsize=TICKS_FONTSIZE,
                     ticks_length=TICKS_LENGTH, ticks_width=TICKS_WIDTH, ticks_color=TICKS_COLOR,
                     ticks_label_xpad=TICKS_LABEL_XPAD, ticks_label_ypad=TICKS_LABEL_YPAD,
                     show_ticks=True, orientation='vertical'):
        self.cax_dim_list = [self.parentframe.left + self.left + cleft, self.parentframe.bottom + self.bottom + cbottom,
                             cwidth, cheight]
        self.cax = self.mainframe.fig.add_axes(np.array(self.cax_dim_list) / self.mainframe.fig_div_list)
        self.mainframe.fig.colorbar(self.imshow, cax=self.cax, orientation=orientation)
        self.cax.tick_params(axis='x', labelsize=ticks_fontsize, direction='in',
                             length=ticks_length, width=ticks_width, color=ticks_color,
                             pad=ticks_label_xpad)
        self.cax.tick_params(axis='y', labelsize=ticks_fontsize, direction='in',
                             length=ticks_length, width=ticks_width, color=ticks_color,
                             pad=ticks_label_ypad)
        if not show_ticks:
            self.cax.set_axis_off()

    def modify_colorbar(self, ticks_fontsize=TICKS_FONTSIZE, ticks_direction=TICKS_DIRECTION,
                        ticks_length=TICKS_LENGTH, ticks_width=TICKS_WIDTH, ticks_color=TICKS_COLOR,
                        show_ticks=True):
        self.cax.tick_params(axis='y', labelsize=ticks_fontsize, direction=ticks_direction,
                             length=ticks_length, width=ticks_width, color=ticks_color)
        self.cax.tick_params(axis='x', labelsize=ticks_fontsize, direction=ticks_direction,
                             length=ticks_length, width=ticks_width, color=ticks_color)
        if not show_ticks:
            self.cax.tick_params(axis='y', left=False, labelleft=False, right=False, labelright=False)
            # self.cax.tick_params(right=False)
            self.cax.tick_params(axis='x', bottom=False, labelbottom=False, top=False, labeltop=False)
            # self.cax.tick_params(ltop=False)

    def fix_xaxis_interval(self, interval):
        self.ax.xaxis.set_major_locator(ticker.MultipleLocator(interval))
    
    def fix_xaxis_top_interval(self, interval):
        self.ax_top.xaxis.set_major_locator(ticker.MultipleLocator(interval))

    def fix_yaxis_interval(self, interval):
        self.ax.yaxis.set_major_locator(ticker.MultipleLocator(interval))
    
    def fix_yaxis_right_interval(self, interval):
        self.ax_right.yaxis.set_major_locator(ticker.MultipleLocator(interval))

    def assign_image(self, image, extent,
                     xmin, xmax, ymin, ymax, colormap, clim,
                     transpose=False, inversex=False, inversey=False,
                     origin='lower', interpolation='none', func_colormap=None,
                     norm=None):
        self.ax.set_xlim(xmin, xmax)
        self.ax.set_ylim(ymin, ymax)
        aspect_ = (self.ax_dim_list[3] / self.ax_dim_list[2]) * np.abs(xmax - xmin) / np.abs(ymax - ymin)
        if callable(func_colormap):
            colormap = func_colormap(colormap)
        image_ = image
        if transpose:
            image_ = image_.T
        if inversex:
            image_ = image_[:, ::-1]
        if inversey:
            image_ = image_[::-1, :]
        imshow_ = self.ax.imshow(image_, origin=origin, interpolation=interpolation, aspect=aspect_, extent=extent,
                                 cmap=plt.get_cmap(colormap), clim=clim, norm=norm)
        self.imshow = imshow_

    def assign_general_image(self, image):
        row_, column_ = image[:, :, 0].shape
        extent_ = [0, row_, 0, column_]
        self.ax.set_xlim(0, row_)
        self.ax.set_ylim(0, column_)
        aspect_ = (self.ax_dim_list[3] / self.ax_dim_list[2]) * np.abs(row_) / np.abs(column_)
        self.ax.imshow(image, aspect=aspect_, extent=extent_)

    def set_arrow_yaxis(self, arrow_color='black', arrow_lw=0.75,
                        arrow_head_width=0.04, arrow_head_length=0.08, arrow_overhang=0.0,
                        pos_axis_start=0.0, pos_axis_end=1.0):
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.tick_params(axis='y', right=False)
        y0_, y1_ = self.ax.get_ylim()
        n_ticks_invisible = np.argwhere(self.ax.get_yticks() >= y0_)[0][0]
        tmp_yticks_visible_ = [t_ for t_ in self.ax.get_yticks() if y0_ <= t_ <= y1_]
        tmp_yticks_pos_ = np.vstack((np.zeros(len(tmp_yticks_visible_)), tmp_yticks_visible_)).T
        yticks_rel_pos_ = self.ax.transAxes.inverted().transform(self.ax.transData.transform(tmp_yticks_pos_))[:, 1]
        for idx_ticks_, tick_rel_pos_ in enumerate(yticks_rel_pos_):
            if pos_axis_end <= tick_rel_pos_:
                self.ax.yaxis.get_major_ticks()[int(idx_ticks_ + n_ticks_invisible)].set_visible(False)
        self.ax.arrow(0, pos_axis_start, 0, pos_axis_end - pos_axis_start,
                      facecolor=arrow_color, edgecolor=arrow_color, lw=arrow_lw,
                      head_width=0, head_length=0, overhang=0,
                      length_includes_head=False, clip_on=False, transform=self.ax.transAxes)
        self.ax.arrow(0, pos_axis_start, 0, pos_axis_end - pos_axis_start,
                      facecolor=arrow_color, edgecolor='none', lw=0,
                      head_width=arrow_head_width, head_length=arrow_head_length, overhang=arrow_overhang,
                      length_includes_head=False, clip_on=False, transform=self.ax.transAxes)

    def set_arrow_xaxis(self, arrow_color='black', arrow_lw=0.75,
                        arrow_head_width=0.04, arrow_head_length=0.08, arrow_overhang=0.0,
                        pos_axis_start=0.0, pos_axis_end=1.0):
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.tick_params(axis='x', top=False)
        x0_, x1_ = self.ax.get_xlim()
        n_ticks_invisible = np.argwhere(self.ax.get_xticks() >= x0_)[0][0]
        tmp_xticks_visible_ = [t_ for t_ in self.ax.get_xticks() if x0_ <= t_ <= x1_]
        tmp_xticks_pos_ = np.vstack((np.zeros(len(tmp_xticks_visible_)), tmp_xticks_visible_)).T
        xticks_rel_pos_ = self.ax.transAxes.inverted().transform(self.ax.transData.transform(tmp_xticks_pos_))[:, 1]
        for idx_ticks_, tick_rel_pos_ in enumerate(xticks_rel_pos_):
            if pos_axis_end <= tick_rel_pos_:
                self.ax.xaxis.get_major_ticks()[int(idx_ticks_ + n_ticks_invisible)].set_visible(False)
        self.ax.arrow(pos_axis_start, 0, pos_axis_end - pos_axis_start, 0,
                      facecolor=arrow_color, edgecolor=arrow_color, lw=arrow_lw,
                      head_width=0, head_length=0, overhang=0,
                      length_includes_head=False, clip_on=False, transform=self.ax.transAxes)
        self.ax.arrow(pos_axis_start, 0, pos_axis_end - pos_axis_start, 0,
                      facecolor=arrow_color, edgecolor='none', lw=0,
                      head_width=arrow_head_width, head_length=arrow_head_length, overhang=arrow_overhang,
                      length_includes_head=False, clip_on=False, transform=self.ax.transAxes)


class PlotFrameMulti:
    def __init__(self, mainframe, parentframe, left, bottom, width, height,
                 nhorizontal, nvertical, horizontaloffset, verticaloffset,
                 ticks_fontsize=TICKS_FONTSIZE, ticks_direction=TICKS_DIRECTION,
                 ticks_length=TICKS_LENGTH, ticks_width=TICKS_WIDTH, ticks_color=TICKS_COLOR,
                 ticks_label_xpad=TICKS_LABEL_XPAD, ticks_label_ypad=TICKS_LABEL_YPAD):
        self.mainframe = mainframe
        self.parentframe = parentframe
        self.left = left
        self.bottom = bottom
        self.width = width
        self.height = height
        self.nhorizontal = nhorizontal
        self.nvertical = nvertical
        self.horizontaloffset = horizontaloffset
        self.verticaloffset = verticaloffset

        self.ax_dim_lists = []
        self.axes = []
        for idh_ in range(self.nhorizontal):
            self.ax_dim_lists.append([])
            self.axes.append([])
            for idv_ in range(self.nvertical):
                frame_dim_list_ = [self.parentframe.left + self.left + self.horizontaloffset * idh_,
                                   self.parentframe.bottom + self.bottom + self.verticaloffset * idv_,
                                   self.width, self.height]
                self.ax_dim_lists[idh_].append(frame_dim_list_)
                ax_ = self.mainframe.fig.add_axes(np.array(frame_dim_list_) / self.mainframe.fig_div_list)
                self.axes[idh_].append(ax_)
        # can be referred as axes[idh][idv] and frame_dim_lists[idh][idv]

        # default appearance
        for idh_ in range(self.nhorizontal):
            for idv_ in range(self.nvertical):
                self.axes[idh_][idv_].tick_params(axis='x', labelsize=ticks_fontsize, direction=ticks_direction,
                                                  length=ticks_length, width=ticks_width, color=ticks_color,
                                                  top=True, pad=ticks_label_xpad)
                self.axes[idh_][idv_].tick_params(axis='y', labelsize=ticks_fontsize, direction=ticks_direction,
                                                  length=ticks_length, width=ticks_width, color=ticks_color,
                                                  right=True, pad=ticks_label_ypad)

        # no top and right axes by default
        self.axes_top = []
        self.axes_right = []
        for idh_ in range(self.nhorizontal):
            self.axes_top.append([])
            self.axes_right.append([])
            for idv_ in range(self.nvertical):
                self.axes_top[idh_].append(None)
                self.axes_right[idh_].append(None)
        # no imshow by default
        self.imshows = []
        for idh_ in range(self.nhorizontal):
            self.imshows.append([])
            for idv_ in range(self.nvertical):
                self.imshows[idh_].append(None)
        # no color bar by default
        self.cax_dim_lists = []
        self.caxes = []
        for idh_ in range(self.nhorizontal):
            self.cax_dim_lists.append([])
            self.caxes.append([])
            for idv_ in range(self.nvertical):
                self.cax_dim_lists[idh_].append([])
                self.caxes[idh_].append(None)

    def add_right_axis(self, idh, idv, ticks_fontsize=TICKS_FONTSIZE, ticks_direction=TICKS_DIRECTION,
                       ticks_length=TICKS_LENGTH, ticks_width=TICKS_WIDTH, ticks_color=TICKS_COLOR):
        self.axes_right[idh][idv] = self.axes[idh][idv].twinx()
        self.axes[idh][idv].tick_params(axis='y', right=False)
        self.axes_right[idh][idv].tick_params(axis='y', labelsize=ticks_fontsize, direction=ticks_direction,
                                              length=ticks_length, width=ticks_width, color=ticks_color)

    def add_top_axis(self, idh, idv, ticks_fontsize=TICKS_FONTSIZE, ticks_direction=TICKS_DIRECTION,
                     ticks_length=TICKS_LENGTH, ticks_width=TICKS_WIDTH, ticks_color=TICKS_COLOR):
        self.axes_top[idh][idv] = self.axes[idh][idv].twiny()
        self.axes[idh][idv].tick_params(axis='x', top=False)
        self.axes_top[idh][idv].tick_params(axis='x', labelsize=ticks_fontsize, direction=ticks_direction,
                                            length=ticks_length, width=ticks_width, color=ticks_color)

    def modify_ticks(self, idh, idv,
                     ticks_fontsize=TICKS_FONTSIZE,
                     ticks_direction=TICKS_DIRECTION, reflect_top=True, reflect_right=True,
                     ticks_length=TICKS_LENGTH, ticks_width=TICKS_WIDTH, ticks_color=TICKS_COLOR,
                     ticks_label_xpad=TICKS_LABEL_XPAD, ticks_label_ypad=TICKS_LABEL_YPAD):
        self.axes[idh][idv].tick_params(axis='x', labelsize=ticks_fontsize, direction=ticks_direction,
                                        length=ticks_length, width=ticks_width, color=ticks_color,
                                        top=reflect_top, pad=ticks_label_xpad)
        self.axes[idh][idv].tick_params(axis='y', labelsize=ticks_fontsize, direction=ticks_direction,
                                        length=ticks_length, width=ticks_width, color=ticks_color,
                                        right=reflect_right, pad=ticks_label_ypad)
        if self.axes_right[idh][idv] is not None:
            self.axes[idh][idv].tick_params(axis='y', right=False)
            self.axes_right[idh][idv].tick_params(axis='y', labelsize=ticks_fontsize, direction=ticks_direction,
                                                  length=ticks_length, width=ticks_width, color=ticks_color)
        if self.axes_top[idh][idv] is not None:
            self.axes[idh][idv].tick_params(axis='x', top=False)
            self.axes_top[idh][idv].tick_params(axis='x', labelsize=ticks_fontsize, direction=ticks_direction,
                                                length=ticks_length, width=ticks_width, color=ticks_color)

    def modify_ticks_all(self, ticks_fontsize=TICKS_FONTSIZE,
                         ticks_direction=TICKS_DIRECTION, reflect_top=True, reflect_right=True,
                         ticks_length=TICKS_LENGTH, ticks_width=TICKS_WIDTH, ticks_color=TICKS_COLOR,
                         ticks_label_xpad=TICKS_LABEL_XPAD, ticks_label_ypad=TICKS_LABEL_YPAD):
        for idh_ in range(self.nhorizontal):
            for idv_ in range(self.nvertical):
                self.axes[idh_][idv_].tick_params(axis='x', labelsize=ticks_fontsize, direction=ticks_direction,
                                                  length=ticks_length, width=ticks_width, color=ticks_color,
                                                  top=reflect_top, pad=ticks_label_xpad)
                self.axes[idh_][idv_].tick_params(axis='y', labelsize=ticks_fontsize, direction=ticks_direction,
                                                  length=ticks_length, width=ticks_width, color=ticks_color,
                                                  right=reflect_right, pad=ticks_label_ypad)
                if self.axes_right[idh_][idv_] is not None:
                    self.axes[idh_][idv_].tick_params(axis='y', right=False)
                    self.axes_right[idh_][idv_].tick_params(axis='y', labelsize=ticks_fontsize,
                                                            direction=ticks_direction,
                                                            length=ticks_length, width=ticks_width, color=ticks_color)
                if self.axes_top[idh_][idv_] is not None:
                    self.axes[idh_][idv_].tick_params(axis='x', top=False)
                    self.axes_top[idh_][idv_].tick_params(axis='x', labelsize=ticks_fontsize,
                                                          direction=ticks_direction,
                                                          length=ticks_length, width=ticks_width, color=ticks_color)

    def add_colorbar(self, idh, idv, cleft, cbottom, cwidth, cheight,
                     ticks_fontsize=TICKS_FONTSIZE, ticks_direction=TICKS_DIRECTION,
                     ticks_length=TICKS_LENGTH, ticks_width=TICKS_WIDTH, ticks_color=TICKS_COLOR,
                     show_ticks=True):
        self.cax_dim_lists[idh][idv] = [self.parentframe.left + self.left + self.horizontaloffset * idh + cleft,
                                        self.parentframe.bottom + self.bottom + self.verticaloffset * idv
                                        + cbottom,
                                        cwidth, cheight]
        self.caxes[idh][idv] = self.mainframe.fig.add_axes(np.array(self.cax_dim_lists[idh][idv])
                                                           / self.mainframe.fig_div_list)
        self.mainframe.fig.colorbar(self.imshows[idh][idv], cax=self.caxes[idh][idv])
        self.caxes[idh][idv].tick_params(axis='y', labelsize=ticks_fontsize, direction=ticks_direction,
                                         length=ticks_length, width=ticks_width, color=ticks_color)
        if not show_ticks:
            self.caxes[idh][idv].set_axis_off()

    def modify_colorbar(self, idh, idv,
                        ticks_fontsize=TICKS_FONTSIZE, ticks_direction=TICKS_DIRECTION,
                        ticks_length=TICKS_LENGTH, ticks_width=TICKS_WIDTH, ticks_color=TICKS_COLOR,
                        show_ticks=True):
        self.caxes[idh][idv].tick_params(axis='y', labelsize=ticks_fontsize, direction=ticks_direction,
                                         length=ticks_length, width=ticks_width, color=ticks_color)
        if not show_ticks:
            self.caxes[idh][idv].set_axis_off()

    def assign_image(self, idh, idv, image, extent,
                     xmin, xmax, ymin, ymax, colormap, clim,
                     transpose=False, inversex=False, inversey=False,
                     origin='lower', interpolation='none', func_colormap=None):
        self.axes[idh][idv].set_xlim(xmin, xmax)
        self.axes[idh][idv].set_ylim(ymin, ymax)
        aspect_ = (self.ax_dim_lists[idh][idv][3] / self.ax_dim_lists[idh][idv][2]) \
                  * np.abs(xmax - xmin) / np.abs(ymax - ymin)
        if callable(func_colormap):
            colormap = func_colormap(colormap)
        image_ = image
        if transpose:
            image_ = image_.T
        if inversex:
            image_ = image_[:, ::-1]
        if inversey:
            image_ = image_[::-1, :]
        imshow_ = self.axes[idh][idv].imshow(image_,
                                             origin=origin, interpolation=interpolation,
                                             aspect=aspect_,
                                             extent=extent,
                                             cmap=plt.get_cmap(colormap),
                                             clim=clim)
        self.imshows[idh][idv] = imshow_

    @staticmethod
    def validate_attribute_tuple(attribute, list_image):
        if isinstance(attribute, tuple):
            if len(attribute) != len(list_image):
                tuple_ = ()
                for i_ in range(len(list_image)):
                    tuple_ += (attribute[0],)
                return tuple_
            else:
                return attribute
        else:
            tuple_ = ()
            for i_ in range(len(list_image)):
                tuple_ += (attribute,)
            return tuple_

    def assign_multi_image_vertical(self, idh, list_image,
                                    tuple_extent, tuple_xmin, tuple_xmax, tuple_ymin, tuple_ymax,
                                    tuple_colormap, tuple_clim,
                                    transpose=False, inversex=False, inversey=False,
                                    origin='lower', interpolation='none', func_colormap=None):
        if np.array(list_image).shape[0] != self.nvertical:
            print('The size of the multiple image complex does not match the multiplot frame size.')
            return
        else:
            tuple_extent = self.validate_attribute_tuple(tuple_extent, list_image)
            tuple_xmin = self.validate_attribute_tuple(tuple_xmin, list_image)
            tuple_xmax = self.validate_attribute_tuple(tuple_xmax, list_image)
            tuple_ymin = self.validate_attribute_tuple(tuple_ymin, list_image)
            tuple_ymax = self.validate_attribute_tuple(tuple_ymax, list_image)
            tuple_colormap = self.validate_attribute_tuple(tuple_colormap, list_image)
            if callable(func_colormap):
                tuple_colormap = func_colormap(tuple_colormap)
            tuple_clim = self.validate_attribute_tuple(tuple_clim, list_image)

            for idv_ in range(self.nvertical):
                # extent_ = image_multi.get_extent()
                self.axes[idh][idv_].set_xlim(tuple_xmin[idv_], tuple_xmax[idv_])
                self.axes[idh][idv_].set_ylim(tuple_ymin[idv_], tuple_ymax[idv_])
                aspect_ = (self.ax_dim_lists[idh][idv_][3]
                           / self.ax_dim_lists[idh][idv_][2]) \
                          * np.abs(tuple_xmax[idv_] - tuple_xmin[idv_]) / np.abs(tuple_ymax[idv_] - tuple_ymin[idv_])
                image_ = list_image[idv_]
                if transpose:
                    image_ = image_.T
                if inversex:
                    image_ = image_[:, ::-1]
                if inversey:
                    image_ = image_[::-1, :]
                imshow_ = self.axes[idh][idv_].imshow(image_,
                                                      origin=origin, interpolation=interpolation,
                                                      aspect=aspect_,
                                                      extent=tuple_extent[idv_],
                                                      cmap=plt.get_cmap(tuple_colormap[idv_]),
                                                      clim=tuple_clim[idv_])
                self.imshows[idh][idv_] = imshow_

    def assign_multi_image_horizontal(self, idv, list_image,
                                      tuple_extent, tuple_xmin, tuple_xmax, tuple_ymin, tuple_ymax,
                                      tuple_colormap, tuple_clim,
                                      transpose=False, inversex=False, inversey=False,
                                      origin='lower', interpolation='none', func_colormap=None):
        if np.array(list_image).shape[0] != self.nhorizontal:
            print('The size of the multiple image complex does not match the multiplot frame size.')
            return
        else:
            tuple_extent = self.validate_attribute_tuple(tuple_extent, list_image)
            tuple_xmin = self.validate_attribute_tuple(tuple_xmin, list_image)
            tuple_xmax = self.validate_attribute_tuple(tuple_xmax, list_image)
            tuple_ymin = self.validate_attribute_tuple(tuple_ymin, list_image)
            tuple_ymax = self.validate_attribute_tuple(tuple_ymax, list_image)
            tuple_colormap = self.validate_attribute_tuple(tuple_colormap, list_image)
            if callable(func_colormap):
                tuple_colormap = func_colormap(tuple_colormap)
            tuple_clim = self.validate_attribute_tuple(tuple_clim, list_image)

            for idh_ in range(self.nhorizontal):
                # extent_ = image_multi.get_extent()
                self.axes[idh_][idv].set_xlim(tuple_xmin[idh_], tuple_xmax[idh_])
                self.axes[idh_][idv].set_ylim(tuple_ymin[idh_], tuple_ymax[idh_])
                aspect_ = (self.ax_dim_lists[idh_][idv][3]
                           / self.ax_dim_lists[idh_][idv][2]) \
                          * np.abs(tuple_xmax[idh_] - tuple_xmin[idh_]) / np.abs(tuple_ymax[idh_] - tuple_ymin[idh_])
                image_ = list_image[idh_]
                if transpose:
                    image_ = image_.T
                if inversex:
                    image_ = image_[:, ::-1]
                if inversey:
                    image_ = image_[::-1, :]
                imshow_ = self.axes[idh_][idv].imshow(image_,
                                                      origin=origin, interpolation=interpolation,
                                                      aspect=aspect_,
                                                      extent=tuple_extent[idh_],
                                                      cmap=plt.get_cmap(tuple_colormap[idh_]),
                                                      clim=tuple_clim[idh_])
                self.imshows[idh_][idv] = imshow_
